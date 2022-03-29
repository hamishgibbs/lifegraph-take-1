from utils import (
    read_json,
    parse_date,
    daterange_includes_now_parsed
)

def get_id_from_list(id, l):
    res = [x for x in l if x["@id"] == id]
    try:
        assert len(res) == 1
    except AssertionError:
        raise Exception(f"Found multiple ids: {id}.")
    return res[0]

def resolve_id(id, type):
    entities = read_json(f"./graph/{type}.json")
    return get_id_from_list(id, entities)

def flat(ll):
    return [item for sublist in ll for item in sublist]

def f7(seq):
    """Return an ordered set from a list of duplicates."""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def which_match(l1, l2):
    res = []
    for i1 in l1:
        res.append([i for i, x in enumerate(l2) if i1 == x][0])
    return res

def author_affiliation_text(id): # author_list
    author_list = resolve_id(id, "author_list")

    content = []

    for person in author_list["person"]:
        person = resolve_id(person, "person")
        name_formatted = f'{person["first_name"]} {person["last_name"]}'
        affiliations = []
        for department in person["department"]:
            if daterange_includes_now_parsed(**department):
                department = resolve_id(department["id"], "department")
                university = resolve_id(department["university"], "university")
                affiliation_text = f'{department["name"]}, {university["name"]}, {university["city"]}, {university["country"]}.'
                affiliations.append(affiliation_text)
        content.append((name_formatted, affiliations))

    ordered_affiliations = f7(flat([x[1] for x in content]))

    authors = []
    for author in content:
        affiliation_index = [str(x + 1) for x in sorted(which_match(author[1], ordered_affiliations))]
        authors.append(author[0] + f'<sup>{",".join(affiliation_index)}</sup>')

    affiliations = []
    for i, affiliation in enumerate(ordered_affiliations):
        affiliations.append(f'<sup>{i+1}</sup>{affiliation}')

    text = ", ".join(authors) + "</br></br>" + "</br>".join(affiliations)
    with open("output/author_affiliation_text.html", "w") as f:
        f.write(text)


def main():
    author_affiliation_text("paper#1")

if __name__ == "__main__":
    main()
