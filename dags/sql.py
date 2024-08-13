from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("DagApp") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.sql("SHOW DATABASES").show()


