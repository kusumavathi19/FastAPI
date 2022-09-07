from importlib.metadata import metadata
from urllib import response
import pandas as pd
from pyspark.sql import SparkSession,SQLContext
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base, sessionmaker,decl_api
import extract,sys
from fastapi import FastAPI,Form,status,responses
#import spark_connection

DB_URL = "oracle://kusuma:kusuma@localhost:1521/xe"
engine = create_engine(DB_URL)
connection=engine.connect()
SessionLocal = sessionmaker(bind=engine)
db=SessionLocal()


app = FastAPI()


@app.post("/login/")
async def login(server: str = Form(),database: str = Form(),username: str = Form(),password: str = Form()):
    DB_URL = "oracle+cx_oracle://system:oracle@localhost:1521/xe"
    engine = create_engine(DB_URL)
    connection=engine.connect()
    if server =='localhost' and database == 'xe' and username == 'kusuma' and password == 'kusuma':
        return {"username": username, "inform":"CONNECTED"}
    else:
        responses.status_code = status.HTTP_404_NOT_FOUND
        return{'details':f"Connection failed"}
        

#retrieving schemas
@app.get("/schemas")
async def schema():
    inspector=inspect(engine)
    result=inspector.get_schema_names()
    return result

#retrieving table names
@app.get("/tables")
async def get_tables(schema_name:str):
    inspector =inspect(engine)
    result=inspector.get_table_names(schema_name)
    if not result:
        responses.status_code = status.HTTP_404_NOT_FOUND
        return{'details':f"{schema_name} is not available"}
    return result

#retriving metadata
@app.get("/metadata")
def get_metadata(table_name:str):
    inspector =inspect(engine)
    result=inspector.get_columns(table_name)
    if not result:
        responses.status_code = status.HTTP_404_NOT_FOUND
        return{'details':f"table with table name {table_name} is not available"}
    return result


# @app.get("/parquet_file")
# def get_dict(obj: extract.Base):
#     fields = dict(vars(obj))
#     del fields["_sa_instance_state"]
#     return fields


# tables = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules["extract"]) if inspect.isclass(
#     cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]

# for table in tables:
#     print("---------------------------------------------------------------------")
#     print("                 ", table.__name__)
#     print("---------------------------------------------------------------------")
#     result = db.query(table).all()
#     result = list(map(get_dict, result))
#     df = spark_connection.spark.createDataFrame(result)
#     df.repartition(1).write.parquet(f"parquet_output/{table.__name__}")
