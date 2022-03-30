import re
from utils import (
    resolve_id,
    flat
)

def email_for_author_list(email_template, author_list, custom_content):
    email_template = resolve_id(email_template)
    author_list = resolve_id(author_list)

    adressees = [resolve_id(x) for x in author_list["authors"]]

    template_fields = set(re.findall('{(.+?)}',email_template["body"]))

    try:
        assert len(template_fields.difference(set(custom_content.keys()))) == 0
    except AssertionError:
        raise Exception(f'custom_content does not contain all expected fields: {", ".join(template_fields)}')

    email_body = "<strong>Email content:</strong></br></br>" + email_template["body"].format(**custom_content)

    email_adresses = []
    for adressee in adressees:
        if type(adressee["email"]) is list:
            email_adresses.append(adressee["email"])
        else:
            email_adresses.append([adressee["email"]])

    email_adresses = [f"<a href='mailto:{x}'>{x}</a>" for x in flat(email_adresses)]

    adress_prompt = "<strong>Addressed to:</strong></br></br>" + ", ".join(email_adresses)

    text = "</br></br>".join([adress_prompt, email_body])

    with open("output/email_template_for_authors.html", "w") as f:
        f.write(text)

def main():
        custom_content = {
            "newline": "</br>",
            "manuscript_title": "on Ebola in Panda Bears",
            "manuscript_link": "<a href='https://docs.google.com/document/d/1fkHd7wyCbNW_QwB0o5cfL1t1WCqoB5YV5vaFKmM3O7w/edit'>https://docs.google.com/document/d/1fkHd7wyCbNW_QwB0o5cfL1t1WCqoB5YV5vaFKmM3O7w/edit</a>",
            "review_deadline": "Friday, April 20th"
        }
        email_for_author_list(
            "author_preliminary_review",
            "paper#1",
            custom_content
        )

if __name__ == "__main__":
    main()
