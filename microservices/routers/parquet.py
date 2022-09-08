#import connections
from connections import conn_string, create_engine
from sqlalchemy.orm import decl_api, sessionmaker
import os, subprocess, colorama, importlib, sys, inspect
from pyspark.sql import SparkSession
from fastapi import HTTPException
from typing import List
import spark_connection

# colorama.init(autoreset=True)
# os.environ["SPARK_HOME"] = "C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2"
# os.environ["HADOOP_HOME"] ="C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop"
# os.environ["PATH"] += ";C:\\Users\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\hadoop\\bin"
# os.environ["PYSPARK_PYTHON"] ="C:\\Users\\Kusuma\\FastAPI\\Scripts\\python"



# spark = SparkSession.builder.appName("Local Creator").getOrCreate()

def get_dict(obj: decl_api.DeclarativeMeta):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields


def create_parquet(engine, schemas:List[str], table:List[str]=[], path:str="dest", compression:str="snappy"):
    for schema in schemas:
        url= conn_string+schema
        print(colorama.Fore.GREEN+"INFO:","\t  Connection URL : ",url)
        engine =create_engine(url)
        SessionLocal = sessionmaker(bind=engine)
        sqla_path = os.getcwd()+"\\env\\Scripts\\sqlacodegen.exe"
        print(colorama.Fore.GREEN+"INFO:",f"\t  Running Command : {sqla_path} {url} --outfile {schema}.py")
        subprocess.Popen([sqla_path, url, "--outfile", f"{schema}.py"]).wait()
        table_module = importlib.__import__(schema)
        importlib.reload(table_module)
        if not table:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]
            for table in tables:
                db = SessionLocal()    
                result = db.query(table).all()
                result = list(map(get_dict, result))
                try:
                    df =spark_connection.spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",f"\t  Writing {table.__name__} to {path} using {compression}")
                    df.repartition(1).write.mode("overwrite").format("parquet").option("compression", compression).save(f"{path}/{table.__name__}")
                except ValueError:
                    raise HTTPException(status_code=500, detail=f"Cannot infer Column Datatypes for Table {table}, Please provide the schema manually.")
        else:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base" and cls_obj.__tablename__ in table]
            for table in tables:
                db = SessionLocal()    
                result = db.query(table).all()
                result = list(map(get_dict, result))
                try:
                    df = spark_connection.spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",f"\t  Writing {table.__name__} to {path} using {compression}")
                    df.repartition(1).write.mode("overwrite").format("parquet").option("compression", compression).save(f"{path}/{table.__name__}")
                except ValueError:
                    raise HTTPException(status_code=500, detail=f"Cannot infer Column Datatypes for Table {table}, Please provide the schema manually.")
        del table_module
        os.remove(f"{schema}.py")

