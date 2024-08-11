from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    'spark_submit_example',
    default_args=default_args,
    description='DAG para executar um script PySpark via SparkSubmitOperator',
    schedule_interval=None,
) as dag:

    spark_submit_task = SparkSubmitOperator(
        application='/opt/airflow/sql.py',
        task_id='spark_submit_task',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.driver.memory': '2g',
            'spark.executor.memory': '4g',
            'spark.sql.warehouse.dir': 'hdfs://hadoop:9000/user/hive/warehouse',
        },
        application_args=['arg1', 'arg2'],
        verbose=True,
    )

    spark_submit_task
