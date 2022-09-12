from importlib.metadata import metadata
import os
from pyspark.sql import SparkSession
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker,decl_api


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
