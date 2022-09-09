from typing import List
from importlib.metadata import metadata
from pyexpat import model
from urllib import response
import pandas as pd
from pyspark.sql import SparkSession,SQLContext
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base, sessionmaker,decl_api
import extract,sys,inspect as inspect_module
from fastapi import FastAPI,Form,status,responses
import spark_connection
import connections,models
from parquet import create_parquet
from config import config
from parquet import connection_required



# DB_URL = "oracle://kusuma:kusuma@localhost:1521/xe"
# engine = create_engine(DB_URL)
# connection=engine.connect(

app = FastAPI()
app.include_router(connections.router)

# @app.post("/login/")
# @connections.connection_required
# async def login(server: str = Form(),database: str = Form(),username: str = Form(),password: str = Form()):
#     DB_URL = "oracle+cx_oracle://system:oracle@localhost:1521/xe"
#     engine = create_engine(DB_URL)
#     connection=engine.connect()
#     if server =='localhost' and database == 'xe' and username == 'kusuma' and password == 'kusuma':
#         return {"username": username, "inform":"CONNECTED"}
#     else:
#         responses.status_code = status.HTTP_404_NOT_FOUND
#         return{'details':f"Connection failed"}
        

#retrieving schemas
@app.get("/schemas")
async def schema():
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    inspector=inspect(engine)
    result=inspector.get_schema_names()
    return result

#retrieving table names
@app.get("/tables")
async def get_tables(schema_name:str):
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    inspector =inspect(engine)
    result=inspector.get_table_names(schema_name)
    if not result:
        responses.status_code = status.HTTP_404_NOT_FOUND
        return{'details':f"{schema_name} is not available"}
    return result

#retriving metadata
@app.get("/metadata")
async def get_metadata(table_name:str):
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    inspector =inspect(engine)
    result=inspector.get_columns(table_name)
    if not result:
        responses.status_code = status.HTTP_404_NOT_FOUND
        return{'details':f"table with table name {table_name} is not available"}
    return result

# async def get_dict(obj: extract.Base):
#     fields = dict(vars(obj))
#     del fields["_sa_instance_state"]
#     return fields


# tables = [cls_obj for cls_name, cls_obj in inspect_module.getmembers(sys.modules["extract"]) if inspect_module.isclass(
#     cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]



# @app.get("/parquet_file")
# def convert_to_parquet():
#     for table in tables:
#         print("---------------------------------------------------------------------")
#         print("                 ", table.__name__)
#         print("---------------------------------------------------------------------")
#         result = db.query(table).all()
#         result = list(map(get_dict, result))
#         df = spark_connection.spark.createDataFrame(result)
#         df.repartition(1).write.parquet(f"parquet_output1/{table.__name__}")
#         return {"message":"success"}


@app.post("/")
@connection_required
async def archive_all():
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    inspector = inspect(engine)
    schema_names = inspector.get_schema_names()
    create_parquet(engine, schema_names)
    pass


@app.post("/schema")
@connection_required
async def archive_schema(schema: str, archive_details: models.ArchiveInfo):
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    create_parquet(engine, [schema])
    return {"msg": "Creation of parquet files for all tables completed successfully"}


@app.post("/table")
@connection_required
async def archive_table(schema: List[str], table: List[str], archive_details: models.ArchiveInfo):
    engine = config.engine
    create_parquet(engine, schema, table, archive_details)
    return {"msg": "Creation of parquet files for all tables completed successfully"}