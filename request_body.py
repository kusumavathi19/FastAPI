from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
app =FastAPI()
class Package(BaseModel):
    name:str
    number:str
    description:Optional[str]=None
    
@app.post("/package/{priority")    
async def make_package(priority:int,package: Package):
    return{priority:prioackage




class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None





@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}