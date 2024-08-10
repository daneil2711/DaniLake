from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def helloWorld():
    print('Hello caraio')


with DAG(dag_id="hello_world",
         start_date=datetime(2023,1,1),
         schedule="@hourly",
         catchup=False #parametro pra executar somente o ultimo schedule e n desde o start date
         ) as dag:
    
    task1 = PythonOperator(
        task_id="hello_world",
        python_callable=helloWorld
    )

    task1