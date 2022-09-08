from functools import wraps
from typing import Callable, Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from models import DBInfo
from sqlalchemy.orm import sessionmaker

engine = None
connection_details = None


router = APIRouter(prefix="/connect")

@router.post("/")
async def connect(details: DBInfo):
    dialect = "pyodbc"
    if details.database_name == "mysql":
        dialect = "pymysql"
    elif details.database_name == "oracle":
        dialect = "cx_oracle"
    elif details.database_name == "mssql":
        dialect == "pymssql"
    conn_string = f"{details.database_name}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/{details.schema_name}"
    global engine
    global connection_details
    engine = create_engine(conn_string)
    connection_details = details
    if not engine.connect():
        return {"msg": "Wrong or missing Credentials"}
    else:
        return {"msg": "Connection successfull"}


# A decorator to check if a connection exists before calling the passed function
def connection_required(func : Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args:Any, **kwargs:Any):
        global engine
        if not engine:
            raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
        else:
            return func(*args, **kwargs)
    return wrapper