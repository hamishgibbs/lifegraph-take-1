from compute.schema import get_accepted_values

def test_get_accepted_values():

    test_schema = [
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
          "country": "string"
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

    res = get_accepted_values(test_schema[0], test_schema)

    exp = ["organisation", "university", "university_department", "chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])

    res = get_accepted_values(test_schema[2], test_schema)

    exp = ["university_department", "chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])

    res = get_accepted_values(test_schema[3], test_schema)

    exp = ["chemistry_department"]

    assert all([a == b for a, b in zip(sorted(res), sorted(exp))])
