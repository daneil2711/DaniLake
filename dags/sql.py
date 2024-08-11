#Jeito python
# import pyspark
# from delta import *

# builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
#     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
#     .config("spark.sql.warehouse.dir", "hdfs://hadoop:9000/users/hive/warehouse") \
#     .config("spark.driver.memory", "2g") \
#     .config("spark.master", "spark://spark-master:7077") \
#     .enableHiveSupport()

# spark = configure_spark_with_delta_pip(builder).getOrCreate()

# spark.sql('show databases').show()

# Jeito dag

# from pyspark.sql import SparkSession
if __name__ == "__main__":
    # Aqui assumimos que a sessão Spark já foi criada e configurada pela DAG do Airflow
    spark = SparkSession.builder.getOrCreate()

    # Executar o comando SQL para mostrar as bases de dados do Hive
    spark.sql('SHOW DATABASES').show()
