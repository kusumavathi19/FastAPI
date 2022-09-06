from importlib.metadata import metadata
import os,pandas
import pandas as pd
from pyspark.sql import SparkSession,SQLContext
from sqlalchemy import Column, Integer, String, create_engine
import inspect
from sqlalchemy.orm import declarative_base, sessionmaker,decl_api
import extract,sys


#DB_URL="mysql+pymysql://root:estuate@10.10.10.217:3300/classicmodels"
DB_URL = "oracle://kusuma:kusuma@localhost:1521/xe"
engine = create_engine(DB_URL)
connection=engine.connect()
SessionLocal = sessionmaker(bind=engine)
db=SessionLocal()

os.environ["SPARK_HOME"] = "C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2"
os.environ["HADOOP_HOME"] ="C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop"
os.environ["PATH"] += ";C:\\Users\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\hadoop\\bin"
os.environ["PYSPARK_PYTHON"] ="C:\\Users\\Kusuma\\FastAPI\\Scripts\\python"

print("-----------------------------------------ENVIRONMENT VARIABLES---------------------------------------------------")
print(os.environ["spark_home"])
print(os.environ["hadoop_home"])
print(os.environ["pyspark_python"])
print("-----------------------------------------------------------------------------------------------------------------")
spark = SparkSession\
.builder\
.appName("Spark SQL basic example")\
.getOrCreate()

# for table in extract.Base.metadata.tables.keys():
#     print(table)
# pdf=pd.read_sql_table(table,engine)
# print(pdf)
# df =spark.createDataFrame(pdf)
# df.show()
# #df.write.mode("overwrite").option('compression','snappy').parquet('export3.parquet')

def get_dict(obj: extract.Base):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields


tables = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules["extract"]) if inspect.isclass(
    cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]

for table in tables:
    print("---------------------------------------------------------------------")
    print("                 ", table.__name__)
    print("---------------------------------------------------------------------")
    result = db.query(table).all()
    result = list(map(get_dict, result))
    df = spark.createDataFrame(result)
    df.repartition(1).write.parquet(f"parquet_output/{table.__name__}")
