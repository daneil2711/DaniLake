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
    'spark_submit',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    spark_submit_task = SparkSubmitOperator(
        application='/opt/airflow/dags/sql.py',
        task_id='spark_submit_task',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '2g',
            'spark.driver.cores': '2',
            'spark.executor.memory': '2g',
            'spark.executor.cores': '2',
            'spark.cores.max': '4',
            'spark.sql.warehouse.dir': 'hdfs://hadoop:9000/user/hive/warehouse',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
        },
        packages='io.delta:delta-core_2.12:2.1.0',
        application_args=['arg1', 'arg2'],
        verbose=True,
    )

    spark_submit_task
