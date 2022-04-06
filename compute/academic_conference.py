import json
from utils import (
    read_graph_entities_json,
    catch_single_val,
    parse_date,
    Graph
)

def list_todays_conference_events(academic_conference, graph):
    academic_conference = graph.resolve_id(academic_conference)

    formatted_events = []

    for sub_event in catch_single_val(academic_conference["sub_event"]):
        event = graph.resolve_id(sub_event)
        start_f = parse_date(event["start"]).strftime("%-H:%-M")
        end_f = parse_date(event["end"]).strftime("%-H:%-M")
        formatted_events.append(f"{event['name']}: ({start_f}-{end_f})")



def main():
    entities = read_graph_entities_json("./graph/*.json")
    graph = Graph(entities=entities)

    list_todays_conference_events("gisruk_2022", graph)

if __name__ == "__main__":
    main()
