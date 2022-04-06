import json
import sys
import glob
from compute.utils import (
    read_json,
    flat,
    get_id_from_list,
    Graph,
    read_graph_entities_json
)
import networkx as nx
from astropy.time import Time


def get_accepted_values(type, schema):

    G = nx.DiGraph()
    for item in schema:
        G.add_node(item["@id"])

    for item in schema:
        if "@parent" in item.keys():
            G.add_edge(item["@parent"], item["@id"])

    paths = []

    for item in schema:
        paths_from_node = flat(list(nx.all_simple_paths(G, source=type["@id"], target=item["@id"])))
        paths_from_node.append(type["@id"])
        paths.append(paths_from_node)

    return list(set(flat(paths)))

# This could maybe be deprecated
def write_accepted_values_index():
    schema = read_json("./graph/meta/schema.jsonx")
    accepted_values = build_accepted_values_index(schema)
    with open("./graph/meta/accepted_values_index.jsonx", "w") as f:
        json.dump(accepted_values, f, sort_keys=True, indent=4)

def build_accepted_values_index(schema):
    accepted_values = {}
    for xtype in schema:
        accepted_values[xtype["@id"]] = get_accepted_values(xtype, schema)
    return accepted_values

def list_type_properties(type, schema, properties=[]):
    properties.append(type["properties"])
    if "@parent" not in type.keys():
        return properties
    else:
        parent = get_id_from_list(type["@parent"], schema)
        return list_type_properties(parent, schema, properties)

def flat_dict_list(dl):
    return {k: v for d in dl for k, v in d.items()}

# This could maybe be deprecated
def write_property_index():
    schema = read_json("./graph/meta/schema.jsonx")
    property_index = build_property_index(schema)
    with open("./graph/meta/property_index.jsonx", "w") as f:
        json.dump(property_index, f, sort_keys=True, indent=4)

def build_property_index(schema):
    accepted_values = build_accepted_values_index(schema)
    leaf_types = ["string", "number", "date"]
    property_index = {}
    for xtype in schema:
        all_accepted_properties = flat_dict_list(list_type_properties(xtype, schema, properties=[]))
        for k in all_accepted_properties:
            if all_accepted_properties[k] not in leaf_types:
                all_accepted_properties[k] = accepted_values[all_accepted_properties[k]]
        property_index[xtype["@id"]] = all_accepted_properties
    return property_index

def audit_graph_schema_json():
    entities = read_graph_entities_json("./graph/*.json")
    schema = read_json("./graph/meta/schema.jsonx")

    graph = Graph(entities=entities)

    auditer = GraphAuditer(schema=schema, graph=graph)
    auditer.audit_graph_compliance_with_schema(verbose=True)

class GraphAuditer:
    def __init__(self, schema, graph):
        self.graph = graph
        self.property_index = build_property_index(schema)
        self.default_data_keys = ["@id", "@type"]
        self.leaf_types = ["string", "number", "date"]
        self.audit_failures = []
        self.audited_entities = 0
        self.audited_properties = 0

    def audit_graph_compliance_with_schema(self, verbose=False):
        for entity in self.graph.entities:
            self.audited_entities += 1
            self.audited_properties += len(entity.keys())

            if self.check_entity_type_exists_in_schema(type=entity["@type"]):
                if self.check_entity_has_only_known_properties(entity=entity):
                    self.check_entity_property_values(entity=entity)

        if verbose:
            if len(self.audit_failures) == 0:
                print(f"Graph is schema-compliant. Audited {self.audited_entities:,} entities with {self.audited_properties:,} properties.")
            else:
                print("\n".join(self.audit_failures))

        return self.audit_failures

    def check_entity_type_exists_in_schema(self, type):
        try:
            self.property_index[type]
            return True
        except KeyError:
             self.audit_failures.append(f'Schema has no @type: "{type}"')

    def check_entity_has_only_known_properties(self, entity):
        schema_type = self.property_index[entity["@type"]]
        expected_properties = list(schema_type.keys()) + self.default_data_keys
        try:
            key_difference = set(entity.keys()).difference(expected_properties)
            assert len(key_difference) == 0
            return True
        except AssertionError:
            key_difference = ", ".join([f'"{x}"' for x in key_difference])
            self.audit_failures.append(f'Entity @id: "{entity["@id"]}" has unrecognised property(ies): {key_difference}')

    def check_entity_property_values(self, entity):
        for property_name in entity.keys():
            schema_type = self.property_index[entity["@type"]]
            if property_name not in self.default_data_keys:
                accepted_value_types = schema_type[property_name]
                value_content = entity[property_name]

                if type(value_content) is not list:
                    value_content = [value_content]

                for property_value in value_content:
                    if accepted_value_types not in self.leaf_types:
                        self.check_property_value_points_to_expected_type(
                            entity_id=entity["@id"],
                            property_key=property_name,
                            property_value=property_value,
                            accepted_value_types=accepted_value_types)

    def check_property_value_points_to_expected_type(self,
                                                     entity_id,
                                                     property_key,
                                                     property_value,
                                                     accepted_value_types):
        accepted_value_types_formatted = ", ".join([f'"{x}"' for x in accepted_value_types])
        try:
            pointed_entity = self.graph.resolve_id(property_value)
        except AssertionError:
            self.audit_failures.append(
               f'Entity @id: "{entity_id}" property: "{property_key}" points to unknown entity @id: "{property_value}". Expected an entity of @type: {accepted_value_types_formatted}.'
            )
            return
        try:
            assert pointed_entity["@type"] in accepted_value_types
        except AssertionError:
            self.audit_failures.append(
               f'Entity @id: "{entity_id}" property: "{property_key}" points to entity of @type: "{pointed_entity["@type"]}". Expected an entity of @type: {accepted_value_types_formatted}.'
            )
            return

def gen_data_for_type(type, property_index):
    expected_properties = property_index[type["@id"]]

    for k in expected_properties:
        if isinstance(expected_properties[k], list):
            expected_properties[k] = expected_properties[k][0]
        elif expected_properties[k] == "number":
            expected_properties[k] = 100
        elif expected_properties[k] == "date":
            expected_properties[k] = "1-1-2020 00:00:00"

    generated_type = expected_properties
    generated_type["@id"] = type["@id"]
    generated_type["@type"] = type["@id"]
    return generated_type

def gen_data(schema):
    property_index = build_property_index(schema)

    graph = []

    for xtype in schema:
        graph.append(gen_data_for_type(xtype, property_index))

    return json.loads(json.dumps(graph, sort_keys=True, indent=4))
