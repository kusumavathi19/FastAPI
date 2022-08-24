import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{filepath : path}")
async def read_file(filepath:str):
    return{"file_path" :filepath}

