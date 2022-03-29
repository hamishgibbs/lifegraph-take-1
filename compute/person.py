from utils import (
    resolve_id,
    parse_date,
    flat
)

def person_brief_resume(id):
    person = resolve_id(id)
    content=[]
    for affiliation in person["affiliation"]:
        organisation = resolve_id(affiliation["id"])
        if "@parent" in organisation.keys():
            organisation = resolve_id(organisation["@parent"])
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


def main():
    weave_resume_brief_summary(["hamishgibbs", "yangliu", "rozeggo"])

if __name__ == "__main__":
    main()
