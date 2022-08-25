
from fastapi import FastAPI

app = FastAPI()

item_list=[{"items1":"bar"},{"item2":"milk"},{"item3":"water"}]
@app.get("/item_list/")
async def read_item(skip: int=0, limit: int=10):
    return item_list[skip:skip+limit]
    
@app.get("/items/")
async def items(num:int,text:str):
        return{"number":num,"text":text}
    
    
    
  #  from fastapi import FastAPI

##app = FastAPI()

#fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



#@app.get("/items/")
#async def read_item(skip: int = 0, limit: int = 10):
 #   return fake_items_db[skip : skip + limit]