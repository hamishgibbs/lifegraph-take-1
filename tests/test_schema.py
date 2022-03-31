import pytest
import json
from compute.utils import Graph
from compute.schema import (
    get_accepted_values,
    build_accepted_values_index,
    build_property_index,
    audit_graph_schema,
    gen_data,
    GraphAuditer
)

@pytest.fixture()
def mock_schema():
    return [
      {
        "@id": "organisation",
        "properties": {
          "name": "string"
        }
      },
      {
        "@id": "university",
        "@parent": "organisation",
        "properties": {
          "city": "string",
          "country": "string",
          "total_enrollment": "number",
          "founded": "date"
        }
      },
      {
        "@id": "university_department",
        "@parent": "organisation",
        "properties": {
          "parent_organisation": "university"
        }
      },
      {
        "@id": "chemistry_department",
        "@parent": "university_department",
        "properties": {
          "chemistry_field": "string"
        }
      },
    ]


def test_get_accepted_values(mock_schema):

    res = get_accepted_values(mock_schema[0], mock_schema)

    exp = ["organisation", "university", "university_department", "chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])

    res = get_accepted_values(mock_schema[2], mock_schema)

    exp = ["university_department", "chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])

    res = get_accepted_values(mock_schema[3], mock_schema)

    exp = ["chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])

def test_gen_data(mock_schema):

    res = gen_data(mock_schema)

    assert res == [{'@id': 'organisation', '@type': 'organisation', 'name': 'string'}, {'@id': 'university', '@type': 'university', 'city': 'string', 'country': 'string', 'founded': '1-1-2020 00:00:00', 'name': 'string', 'total_enrollment': 100}, {'@id': 'university_department', '@type': 'university_department', 'name': 'string', 'parent_organisation': 'university'}, {'@id': 'chemistry_department', '@type': 'chemistry_department', 'chemistry_field': 'string', 'name': 'string', 'parent_organisation': 'university'}]

@pytest.mark.skip(reason="wait until audit_graph_schema is a class")
def test_gen_data_compliant(mock_schema):

    entities = gen_data(mock_schema)
    graph = Graph(entities=entities)
    property_index = build_property_index(mock_schema)

    res = audit_graph_schema(property_index, graph)

    assert len(res) == 0

def test_check_entity_type_exists_in_schema_fails(mock_schema):
    auditer = GraphAuditer(schema=mock_schema, graph=[])
    auditer.check_entity_type_exists_in_schema("alien")
    assert len(auditer.audit_failures) == 1
    assert auditer.audit_failures[0] == 'Schema has no @type: "alien"'

def test_check_entity_type_exists_in_schema_succeeds(mock_schema):
    auditer = GraphAuditer(schema=mock_schema, graph=[])
    auditer.check_entity_type_exists_in_schema("university")
    assert len(auditer.audit_failures) == 0

def test_check_entity_has_only_known_properties_fails(mock_schema):
    auditer = GraphAuditer(schema=mock_schema, graph=[])
    entity = {"@id": "one", "@type": "university", "unknownproperty": "string"}
    auditer.check_entity_has_only_known_properties(entity)
    assert len(auditer.audit_failures) == 1
    assert auditer.audit_failures[0] == 'Entity @id: "one" has unrecognised property(ies): "unknownproperty"'

def test_check_entity_has_only_known_properties_succeeds(mock_schema):
    auditer = GraphAuditer(schema=mock_schema, graph=[])
    entity = {"@id": "one", "@type": "university", "name": "string"}
    auditer.check_entity_has_only_known_properties(entity)
    assert len(auditer.audit_failures) == 0

def test_check_property_value_points_to_expected_type_wrong(mock_schema):
    graph = Graph(entities=gen_data(mock_schema))
    auditer = GraphAuditer(schema=mock_schema, graph=graph)
    entity = {"@id": "one", "@type": "university_department", "parent_organisation": "chemistry_department"}
    auditer.check_entity_property_values(entity)
    assert len(auditer.audit_failures) == 1
    assert auditer.audit_failures[0] == 'Entity @id: "one" property: "parent_organisation" points to entity of @type: "chemistry_department". Expected an entity of @type: "university".'

def test_check_property_value_points_to_expected_type_missing(mock_schema):
    graph = Graph(entities=gen_data(mock_schema))
    auditer = GraphAuditer(schema=mock_schema, graph=graph)
    entity = {"@id": "one", "@type": "university_department", "parent_organisation": "book"}
    auditer.check_entity_property_values(entity)
    assert len(auditer.audit_failures) == 1
    assert auditer.audit_failures[0] == 'Entity @id: "one" property: "parent_organisation" points to unknown entity @id: "book". Expected an entity of @type: "university".'

def test_check_property_value_points_to_expected_type_succeeds(mock_schema):
    graph = Graph(entities=gen_data(mock_schema))
    auditer = GraphAuditer(schema=mock_schema, graph=graph)
    entity = {"@id": "one", "@type": "university_department", "parent_organisation": "university"}
    auditer.check_entity_property_values(entity)
    assert len(auditer.audit_failures) == 0
