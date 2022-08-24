import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def index(item_id):
    return{"item_id" : item_id}