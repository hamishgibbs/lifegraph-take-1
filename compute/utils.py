import json
from datetime import datetime

def read_json(fn):
    with open(fn, "r") as f:
        return json.load(f)

def parse_date(date):
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
