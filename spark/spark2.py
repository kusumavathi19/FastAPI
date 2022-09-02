import os
from pyspark.sql import SparkSession
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "oracle+cx_oracle://kusuma:kusuma@localhost:1521/xe"
engine = create_engine(DB_URL)
connection=engine.connect()
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class users(Base):
     __tablename__ = "users"
     id = Column(Integer, primary_key = True)
     name = Column(String(30)) 
     email = Column(String(30)) 
     password= Column(String(30)) 

     def __repr__(self) -> str:
        return f"<users id = {self.id}, name = {self.name}, email = {self.email}, password = {self.password}>"
     def dict(self):
        return {"id" : self.id, "name" : self.name, "email" : self.email, "password" : self.password}
db = SessionLocal()    

os.environ["SPARK_HOME"] = "C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2"
os.environ["HADOOP_HOME"] ="C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop"
os.environ["PATH"] += ";C:\\Users\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\hadoop\\bin"
os.environ["PYSPARK_PYTHON"] ="C:\\Users\\Kusuma\\FastAPI\\Scripts\\python"

spark = SparkSession\
.builder\
.appName("Spark SQL basic example")\
.getOrCreate()


result = db.query(users).all()
result_list = []
for users in result:
        result_list.append(users.dict())


df = spark.createDataFrame(result_list)
df.show()
df.write.mode("overwrite").option('compression','snappy').parquet('export.parquet')
