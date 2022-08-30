from  pyspark.sql import SparkSession

spark = SparkSession\
.builder\
.appName("Spark SQL basic example")\
.getOrCreate()


df=spark.read.option('header','true').csv('export.csv')
df.show()
#df.write.option('compression','snappy').parquet('export2.parquet')
df.printSchema()