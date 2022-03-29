import json
from datetime import datetime

def read_json(fn):
    with open(fn, "r") as f:
        return json.load(f)

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
