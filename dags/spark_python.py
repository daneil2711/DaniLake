from airflow import DAG
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from delta import *
from datetime import datetime

def run_spark_job():
    builder = SparkSession.builder.appName("AirflowDag") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.warehouse.dir", "hdfs://hadoop:9000/users/hive/warehouse") \
        .config("spark.driver.memory", "2g") \
        .config("spark.master", "spark://spark-master:7077") \
        .enableHiveSupport()
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sql('SHOW DATABASES').show()


with DAG(dag_id="spark_python",
         start_date=datetime(2023,1,1),
         schedule="@hourly",
         catchup=False #parametro pra executar somente o ultimo schedule e n desde o start date
         ) as dag:
    
    task1 = PythonOperator(
        task_id="show_dbs",
        python_callable=run_spark_job
    )

    task1