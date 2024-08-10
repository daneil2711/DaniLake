import pyspark
from delta import *

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.warehouse.dir", "hdfs://hadoop:9000/users/hive/warehouse") \
    .config("spark.driver.memory", "2g") \
    .enableHiveSupport()

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Coloque aqui as operações que você deseja realizar com o Spark
