import json
import sys
import glob
from utils import (
    read_json,
    flat,
    get_id_from_list,
    resolve_id
)
from index import index_json_graph
import networkx as nx
from functools import partial
from itertools import chain, starmap, product
chaini = chain.from_iterable

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

def build_accepted_values_index():
    schema = read_json("./graph/meta/schema.jsonx")
    accepted_values = {}
    for xtype in schema:
        accepted_values[xtype["@id"]] = get_accepted_values(xtype, schema)
    with open("./graph/meta/accepted_values_index.jsonx", "w") as f:
        json.dump(accepted_values, f, sort_keys=True, indent=4)

def list_type_properties(type, schema, properties=[]):
    properties.append(type["properties"])
    if "@parent" not in type.keys():
        return properties
    else:
        parent = get_id_from_list(type["@parent"], schema)
        return list_type_properties(parent, schema, properties)

def flat_dict_list(dl):
    return {k: v for d in dl for k, v in d.items()}

def build_property_index():
    schema = read_json("./graph/meta/schema.jsonx")
    accepted_values = read_json("./graph/meta/accepted_values_index.jsonx")
    leaf_types = ["string", "number", "date"]
    property_index = {}
    for xtype in schema:
        all_accepted_properties = flat_dict_list(list_type_properties(xtype, schema, properties=[]))
        for k in all_accepted_properties:
            if all_accepted_properties[k] not in leaf_types:
                all_accepted_properties[k] = accepted_values[all_accepted_properties[k]]
        property_index[xtype["@id"]] = all_accepted_properties

    with open("./graph/meta/property_index.jsonx", "w") as f:
        json.dump(property_index, f, sort_keys=True, indent=4)

def audit_value_type_compliance(entity, entity_key, value, expected_type, audit_failures):
    try:
        pointed_entity = resolve_id(value)
        assert pointed_entity["@type"] in expected_type
    except KeyError:
        audit_failures.append(
           f'Entity: "{entity["@id"]}" points to unknown entity "{value}". Expected @type: "{expected_type}".'
        )
    except AssertionError:
        audit_failures.append(
           f'Entity: "{entity["@id"]}" property "{entity_key}" points to entity of @type "{pointed_entity["@type"]}". Expected @type: "{expected_type}".'
        )

def audit_graph_schema():
    graph_fns = glob.glob("./graph/*.json")
    property_index = read_json("./graph/meta/property_index.jsonx")
    default_keys = ["@id", "@type"]
    leaf_types = ["string", "number", "date"]

    audit_failures = []

    audited_entities = 0
    audited_properties = 0

    for fn in graph_fns:
        graph = read_json(fn)
        for entity in graph:
            audited_entities += 1
            audited_properties += len(entity.keys())
            try:
                expected_properties = property_index[entity["@type"]]
            except KeyError:
                 audit_failures.append(
                    f'Schema has no @type: {entity["@type"]}'
                 )
                 continue

            try:
                key_difference = set(entity.keys()).difference(list(expected_properties.keys()) + default_keys)
                assert len(key_difference) == 0
            except AssertionError:
                audit_failures.append(
                   f'Entity: {entity["@id"]} has unrecognised key(s): {", ".join(list(key_difference))}'
                )
                continue

            for entity_key in entity.keys():
                if entity_key not in default_keys:
                    # resolve id and get type
                    expected_type = expected_properties[entity_key]
                    value_content = entity[entity_key]
                    if expected_type not in leaf_types:
                        if type(value_content) is list:
                            for value in value_content:
                                audit_value_type_compliance(entity, entity_key, value, expected_type, audit_failures)
                        else:
                            audit_value_type_compliance(entity, entity_key, value_content, expected_type, audit_failures)


    if len(audit_failures) == 0:
        print(f"Graph is schema-compliant. Audited {audited_entities:,} entities with {audited_properties:,} properties.")
    else:
        print("\n\n".join(audit_failures))

def main():
    index_json_graph("./graph")
    build_accepted_values_index()
    build_property_index()
    audit_graph_schema()

if __name__ == "__main__":
    main()
