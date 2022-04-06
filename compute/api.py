
# start API
# serve any ID as a page at entities/{id}
# return json
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
