import json
import glob
from astropy.time import Time

def read_json(fn):
    with open(fn, "r") as f:
        return json.load(f)

def get_id_from_list(id, l):
    res = [x for x in l if x["@id"] == id]
    try:
        assert not len(res) < 1
    except AssertionError:
        raise AssertionError(f'Could not find id: "{id}".')

    try:
        assert not len(res) > 1
    except AssertionError:
        raise AssertionError(f'Found multiple ids: "{id}".')

    return res[0]

def read_graph_entities_json(path):
    graph_fns = glob.glob(path)

    entities = []
    for fn in graph_fns:
        entities.append(read_json(fn))

    return flat(entities)

class Graph:
    def __init__(self, entities):
        # Option here to load from JSON files or anything else (`load_json_graph("path/*.json")`)
        self.entities = entities

    def resolve_id(self, id):
        return get_id_from_list(id, self.entities)


def catch_single_val(val):
    if not isinstance(val, list):
        val = [val]
    return val


def parse_date(date: str):
    date_patterns = ["%Y", "%d-%m-%Y", "%d-%m-%Y %H:%M", "%d-%m-%Y %H:%M:%S"]
    if date == "thepast":
        return Time(f"-{4713:05}-01-01T00:00:00", format="fits")
    elif date == "thefuture":
        return Time.strptime("9999", "%Y")
    elif " BC" in date:
        year = int(date.split(" ")[0])
        return Time(f"-{year:05}-01-01T00:00:00", format="fits")
    elif " AD" in date:
        year = int(date.split(" ")[0])
        return Time(f"{year:04}-01-01T00:00:00", format="fits")
    else:
        for pattern in date_patterns:
            try:
                return Time.strptime(date, pattern)
            except Exception:
                pass

def daterange_includes_now_parsed(start: str, end: str, **kwargs):
    return daterange_includes_now(
        parse_date(start),
        parse_date(end),
    )


def daterange_includes_now(start: Time, end: Time):
    # is there a clever destructuring of a dict that can be done? Perhaps with kwargs?
    now = Time.now()
    return now >= start and now <= end

def flat(ll):
    return [item for sublist in ll for item in sublist]
