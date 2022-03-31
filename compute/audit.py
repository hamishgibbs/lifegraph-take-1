from schema import GraphAuditer
from compute_testing import ComputeTester
from utils import (
    Graph,
    read_graph_entities_json,
    read_json
)

def main():
    entities = read_graph_entities_json("./graph/*.json")
    schema = read_json("./graph/meta/schema.jsonx")
    graph = Graph(entities=entities)

    auditer = GraphAuditer(schema=schema, graph=graph)
    data_audit = auditer.audit_graph_compliance_with_schema(verbose=True)

    if not data_audit:
        tester = ComputeTester(schema=schema)
        tester.audit_snippets(verbose=True)

if __name__ == "__main__":
    main()
