from fastapi import APIRouter, HTTPException
from copy import deepcopy
from config import config
import asyncio
from functools import wraps
from typing import Any, Callable
from sqlalchemy import create_engine, exc
from models import DBInfo

# connection_details = DBInfo(database_name="mysql", username="root", schema_name="classicmodels", password="estuate", port_number=3300, ip_address="localhost")
# conn_str = f"{connection_details.database_name}+pymysql://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/"


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
    config.conn_str = f"{details.database_name}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/"
    config.engine = create_engine(config.conn_str)
    config.connection_details = deepcopy(details)
    try:
        config.engine = create_engine(config.conn_str)
        config.connection_details = deepcopy(details)
        config.engine.connect()
        return {"message" : "Connection Successfull"}
    except exc.NoSuchModuleError:
        raise HTTPException(status_code=404, detail="Unknown Database Server")
    except exc.OperationalError:
        raise HTTPException(
            status_code=404, detail="Wrong or missing Credentials")
    except exc.InterfaceError:
        raise HTTPException(
            status_code=404, detail="Dialect not specified or Data source name cannot be found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")

# A decorator to check if a connection exists before calling the passed function
def connection_required(func: Callable) -> Callable:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            if not config.engine:
                raise HTTPException(
                    status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return await func(*args, **kwargs)
        return wrapper
    else:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if not config.engine:
                raise HTTPException(
                    status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return func(*args, **kwargs)
        return wrapper