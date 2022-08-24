import uvicorn 
from fastapi import FastAPI

app=FastAPI()
@app.get("/")
def index():
    return{"name" : "hello"}
    
@app.get("/welcome")
def index():
        return{"text" : "welcome to estuate software"}

@app.get("/operations/{num1}/{num2}")
async def arm_operations(num1:int ,num2:int):
        if(num2== 0):
            return{"error" : "zero division erro"}
        else:
            return{"sum":num1+num2 ,"sub" :num1-num2, "mul":num1*num2,"div":num1/num2}
        