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
    'silver_igdb',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    ingestao_silver = SparkSubmitOperator(
        application='/usr/notebooks/IGDB/src/silver/ingestao.py',
        task_id='ingestao_silver',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '20g',
            'spark.driver.cores': '12',
            'spark.executor.memory': '3400m',
            'spark.executor.cores': '2',
            'spark.sql.warehouse.dir': 'hdfs://hadoop:9000/users/hive/warehouse',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
        },
        packages='io.delta:delta-core_2.12:2.4.0,io.delta:delta-storage:2.4.0', 
        application_args=[
        '--table', '{{ dag_run.conf["table"] }}'
        ],
        verbose=True,
    )

    ingestao_silver
