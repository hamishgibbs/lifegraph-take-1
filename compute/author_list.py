from utils import (
    read_json,
    daterange_includes_now_parsed,
    catch_single_val,
    flat
)

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

def write_author_affiliation_text_to_html(author_list, graph):
    text = author_affiliation_text(author_list, graph)
    with open("output/author_affiliation_text.html", "w") as f:
        f.write(text)

def create_affiliation_text_from_university_department(affiliation, graph):
    affiliation = graph.resolve_id(affiliation)
    child_org = graph.resolve_id(affiliation["organisation"])

    university = graph.resolve_id(child_org["university"])
    affiliation_text = f'{child_org["name"]}, {university["name"]}, {university["city"]}, {university["country"]}.'

    return affiliation_text

def author_affiliation_text(author_list, graph): # author_list
    author_list = graph.resolve_id(author_list)

    content = []

    for person in catch_single_val(author_list["authors"]):
        person = graph.resolve_id(person)
        name_formatted = f'{person["first_name"]} {person["last_name"]}'
        affiliations = []

        for affiliation in catch_single_val(person["affiliation"]):
            affiliation = graph.resolve_id(affiliation)
            if daterange_includes_now_parsed(**affiliation):
                affiliation_text = create_affiliation_text_from_university_department(affiliation, graph)
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

    return text


def main():
    author_affiliation_text("paper#1")

if __name__ == "__main__":
    main()
