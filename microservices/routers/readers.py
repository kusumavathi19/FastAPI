from pyspark.sql import SparkSession
import os , sys
def read_file(path:str):
   
    os.environ["SPARK_HOME"] = "C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2"
    os.environ["HADOOP_HOME"] ="C:\\Users\\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop"
    os.environ["PATH"] += ";C:\\Users\Kusuma\\spark-3.2.2-bin-hadoop3.2\\bin\hadoop\\bin"
    os.environ["PYSPARK_PYTHON"] ="C:\\Users\\Kusuma\\FastAPI\\Scripts\\python"
    spark = SparkSession.builder.appName("Parquet Reader").getOrCreate()
    try:
        df = spark.read.parquet(sys.argv[1])
        df.show()
        printSchema=df.printSchema()
        print("The total number of rows read form the archive : ", df.count())
        print("The total number of columns read form the archive : ", len(df.columns))
    except Exception as e:
        print(f"{e}")

read_file(sys.argv[1])