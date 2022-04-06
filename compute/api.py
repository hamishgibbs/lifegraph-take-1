
# start API
# serve any ID as a page at entities/{id}
# return json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from compute.utils import (
    read_graph_entities_json,
    catch_single_val,
    read_json,
    get_id_from_list,
    Graph
)
from compute.schema import (
    build_property_index
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

entities = read_graph_entities_json("./graph/*.json")
schema = read_json("./graph/meta/schema.jsonx")
schema = build_property_index(schema)
graph = Graph(entities=entities)

def transform_entity_for_rendering(entity):
    entity = entity.copy()
    type_schema = schema[entity["@type"]]

    for key in entity.keys():
        if key not in ["@id", "@type"]:
            entity[key] = catch_single_val(entity[key])

    for key in entity.keys():
        if key not in ["@id", "@type"]:
            values = []
            for value in entity[key]:
                expected_type = type_schema[key]
                if expected_type in ["string", "number", "date"]:
                    values.append({"value": value, "link": False})
                else:
                    values.append({"value": value, "link": True})
            entity[key] = values

    return entity


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/entity/{id}", response_class=HTMLResponse)
async def entity(request: Request, id: str):
    entity = graph.resolve_id(id)
    entity = transform_entity_for_rendering(entity)
    return templates.TemplateResponse("entity.html", {"request": request, "entity": entity})

# store colors in graph?
@app.get("/create/{type}", response_class=HTMLResponse)
async def create(request: Request, type: str):
    leaf_types = ["string", "number", "date"]
    print(schema[type])
    return templates.TemplateResponse("create.html", {"request": request, "schema": schema[type], "leaf_types": leaf_types})

# create a form to fill out all properties of a type
# if expected type is not leaf type, suggest entities to point to
    # First - by ID only
    # Second - Try to match a single entity by the text of a value
