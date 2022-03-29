import json

def read_json(fn):
    with open(fn, "r") as f:
        return json.load(f)
