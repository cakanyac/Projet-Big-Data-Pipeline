from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LireCSV").getOrCreate()

df = spark.read.option("header", True).csv("test_hdfs_spark.csv")
df.show()
