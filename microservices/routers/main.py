from logging import raiseExceptions
from typing import List
from importlib.metadata import metadata
from pyexpat import model
from urllib import response
import pandas as pd
from pyspark.sql import SparkSession,SQLContext
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import inspect,exc
from sqlalchemy.orm import declarative_base, sessionmaker,decl_api
import sys,inspect as inspect_module
from fastapi import FastAPI,Form,status,responses,HTTPException
import spark_connection
import connections,models
from parquet import create_parquet
from config import config
from parquet import connection_required
app = FastAPI()
app.include_router(connections.router)

#retrieving schemas
@app.get("/List_schemas")
@connection_required
async def schema():
    inspector=inspect(config.engine)
    result=inspector.get_schema_names()
    return result

#retrieving table names
@app.get("/tables")
@connection_required
async def get_tables(schema_name:str):
    config.engine.execute(f"alter session set current_schema={schema_name}")
    inspector =inspect(config.engine)
    result=inspector.get_table_names(schema_name)
    if not result:
        raise HTTPException(status_code=404,detail="Enter the valid schema")
    return result

#retriving metadata
@app.get("/metadata")
@connection_required
async def get_metadata(table_name:str):
    connection_details = config.connection_details
    inspector =inspect(config.engine)
    result=inspector.get_columns(table_name)
    fields = {"TABLE":table_name}
    for row in result:
            fields[f"{row['name']}"] = f"{row['type']}"
    if not result:
        raise HTTPException(status_code=404,detail="table does not exist in the database")
    return fields


# @app.post("/")
# @connection_required
# async def archive_all():
#     connection_details = config.connection_details
#     engine = create_engine(
#         f"{connection_details.database_name}+cx_oracle://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
#     inspector = inspect(engine)
#     schema_names = inspector.get_schema_names()
#     create_parquet(engine, schema_names)
#     pass


@app.post("/schema")
@connection_required
async def archive_schema(schema: str, archive_details: models.ArchiveInfo):
    create_parquet(config.engine, [schema], details=archive_details)
    return {"msg": "Creation of parquet files for all tables completed successfully"}


@app.post("/table")
@connection_required
async def archive_table(schema: List[str], table: List[str], archive_details: models.ArchiveInfo):
    engine = config.engine
    create_parquet(engine, schema, table, archive_details)
    return {"msg": "Creation of parquet files for all tables completed successfully"}