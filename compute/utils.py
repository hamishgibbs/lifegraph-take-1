import json
from datetime import datetime

def read_json(fn):
    with open(fn, "r") as f:
        return json.load(f)

def get_id_from_list(id, l):
    res = [x for x in l if x["@id"] == id]
    try:
        assert len(res) == 1
    except AssertionError:
        raise Exception(f"Found multiple ids: {id}.")
    return res[0]

def resolve_id(id):
    index = read_json("./graph/meta/index.jsonx")
    entities = read_json(f"./graph/{index[id]}.json")
    return get_id_from_list(id, entities)

def parse_date(date: str):
    date_patterns = ["%Y", "%d-%m-%Y", "%d-%m-%Y %H:%M:%S"]
    if date == "thepast":
        return datetime.min
    elif date == "thefuture":
        return datetime.max
    else:
        for pattern in date_patterns:
            try:
                return datetime.strptime(date, pattern)
            except Exception:
                pass

def daterange_includes_now_parsed(start: str, end: str, **kwargs):
    return daterange_includes_now(
        parse_date(start),
        parse_date(end),
    )


def daterange_includes_now(start: datetime, end: datetime):
    # is there a clever destructuring of a dict that can be done? Perhaps with kwargs?
    now = datetime.now()
    return now >= start and now <= end

def flat(ll):
    return [item for sublist in ll for item in sublist]
