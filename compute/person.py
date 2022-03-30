import sys
from utils import (
    resolve_id,
    parse_date,
    flat
)
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

def person_brief_resume(id):
    person = resolve_id(id)
    content=[]
    for affiliation in person["affiliation"]:
        affiliation = resolve_id(affiliation)

        organisation = resolve_id(affiliation["organisation"])
        if "parent_organisation" in organisation.keys():
            organisation = resolve_id(organisation["parent_organisation"])
        content.append({
            "person": f'{person["first_name"]} {person["last_name"]}',
            "name": organisation["name"],
            "start": parse_date(affiliation["start"]).strftime("%Y"),
            "end": parse_date(affiliation["end"]).strftime("%Y"),
        })
    return content

def resume_brief_summary(id):
    content=person_brief_resume(id)
    res = []
    for item in content:
        res.append(f'{item["name"]} ({item["start"]}-{item["end"]})')

    text = "</br>".join(res)
    with open("output/resume_brief_summary.html", "w") as f:
        f.write(text)

def weave_resume_brief_summary(ids):
    content = []
    for id in ids:
        resume = person_brief_resume(id)
        content.append(resume)
    content = flat(content)

    content = sorted(content, key=lambda d: d['start'])

    res = []
    for i, item in enumerate(content):
        if i > 0:
            res.append("".join(["- </br>"] * ((int(item["start"]) - int(last_start))-1)))
        res.append(f'- {item["person"]}: {item["name"]} ({item["start"]}-{item["end"]})')
        last_start = item["start"]

    text = "</br>".join(res)
    with open("output/weave_resume_brief_summary.html", "w") as f:
        f.write(text)

def create_family_tree(people):
    people = [resolve_id(x) for x in people]
    G = nx.DiGraph()

    for person in people:
        try:
            official_title = person["official_title"]
        except:
            official_title = None

        if official_title:
            name_formatted = f'{official_title} ({person["first_name"]})'
        else:
            name_formatted = f'{person["first_name"]}'

        G.add_node(person["@id"], label=name_formatted)

    for person in people:
        for k in person:
            if k in ["mother", "father", "brother", "son"]:
                G.add_edge(person["@id"], person[k], label=k)

    net = Network(directed =True)
    net.set_edge_smooth('dynamic')
    net.from_nx(G)
    net.show("./output/create_family_tree.html")

def main():
    # resume_brief_summary("hamishgibbs")
    if sys.argv[1] == "weave_resumes":
        weave_resume_brief_summary(["hamishgibbs", "yangliu", "rozeggo"])
    elif sys.argv[1] == "family_tree":
        create_family_tree([
            "zaifeng",
            "yixuan",
            "mianning",
            "puyi",
            "cuiyan",
            "zaitian"
        ])

if __name__ == "__main__":
    main()
