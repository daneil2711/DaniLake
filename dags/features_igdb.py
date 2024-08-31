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
    'features_igdb',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    feature_store_igdb = SparkSubmitOperator(
        application='/usr/notebooks/IGDB/src/silver/feature_store/fs_ingestao.py',
        task_id='feature_store_igdb',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '2g',
            'spark.driver.cores': '2',
            'spark.executor.memory': '2g',
            'spark.executor.cores': '2',
            'spark.sql.warehouse.dir': 'hdfs://hadoop:9000/users/hive/warehouse',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
        },
        packages='io.delta:delta-core_2.12:2.4.0,io.delta:delta-storage:2.4.0', 
        application_args=[
        '--table', '{{ dag_run.conf["table"] }}',
        '--description', '{{ dag_run.conf["description"] }}',
        '--id_fields', '{{ dag_run.conf["id_fields"] }}',
        '--partition_fields', '{{ dag_run.conf["partition_fields"] }}',
        '--date_start', '{{ dag_run.conf["date_start"] }}',
        '--date_stop', '{{ dag_run.conf["date_stop"] }}',
        '--monthly', '{{ dag_run.conf["monthly"] }}'
        ],
        verbose=True,
    )

    feature_store_igdb
