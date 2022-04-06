
# start API
# serve any ID as a page at entities/{id}
# return json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
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

# DEV: this should change from "create" to "edit"
@app.get("/create/{type}", response_class=HTMLResponse)
async def create(request: Request, type: str):
    return templates.TemplateResponse("create.html", {
        "request": request,
        "schema": schema[type],
        "type": type
    })


# store type colors in graph?

@app.get("/suggest_pointed_entity/{type}/{property}/")
async def suggest_pointed_entity(type, property, q):
    print(type, property, search_str)
    raise Exception
    # DEV: search through expected type for specific titles (i.e. name, title, first_name, last_name)
    leaf_types = ["string", "number", "date"]
    expected_pointed_types = schema[type][property]
    print(expected_pointed_types)
    if isinstance(expected_pointed_types, list):
        all_candidates = [x["@id"] for x in graph.entities if x["@type"] in expected_pointed_types]
        search_str_candidates = [x for x in all_candidates if search_str in x]
        return JSONResponse(content=search_str_candidates)
    else:
        return None

# not working to hit suggest_pointed_entity - need to check how $ hits for autocomplete


# DEV: endpoint to recieve form data
# validate that recieved form data complies with schema
