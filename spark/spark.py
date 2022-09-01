from  pyspark.sql import SparkSession
import os


os.environ["SPARK_HOME"] = "C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2"
os.environ["HADOOP_HOME"] ="C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop"
os.environ["PATH"] += ";C:\\Users\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\hadoop\\bin"

spark = SparkSession\
.builder\
.appName("Spark SQL basic example")\
.getOrCreate()
df=spark.read.option('header','true').csv('export.csv')
df.show()
df.write.mode("overwrite").option('compression','snappy').parquet('export1.parquet')
#df.printSchema()

# Select only the "name" column
#df.select("email").show()