import os
import glob
import json
from utils import read_json

def index_json_graph(path):
    # This solution is OK for now but not scalable
    graph_fns = glob.glob(f"{path}/*.json")
    index = []
    for fn in graph_fns:
        entities = read_json(fn)
        for entity in entities:
            try:
                assert entity["@id"] not in [x[0] for x in index]
            except Exception:
                raise Exception(f'Duplicate @id: {entity["@id"]} in {fn}')
            index.append((entity["@id"], os.path.basename(fn).split(".")[0]))
    with open("./graph/index.jsonx", "w") as f:
        json.dump(dict(index), f, sort_keys=True, indent=4)

def main():
    index_json_graph("./graph")

if __name__ == "__main__":
    main()
