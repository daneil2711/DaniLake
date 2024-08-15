from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from hdfs import InsecureClient

def list_hdfs_files():
    from hdfs import InsecureClient
    hdfs_host = 'http://hadoop:9870'
    hdfs_user = 'root'
    client = InsecureClient(hdfs_host, user=hdfs_user)
    files = client.list('/')
    print(files)


with DAG(dag_id="hdfs_list",
         start_date=datetime(2023,1,1),
         schedule="@hourly",
         catchup=False #parametro pra executar somente o ultimo schedule e n desde o start date
         ) as dag:
    
    task1 = PythonOperator(
        task_id="list_hdfs_files",
        python_callable=list_hdfs_files
    )

    task1