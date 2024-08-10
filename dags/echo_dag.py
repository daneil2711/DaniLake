from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.operators.papermill import PapermillOperator
from datetime import datetime

with DAG("teste_echo", 
         start_date=datetime(2021, 1, 1), 
         schedule="@daily", 
         catchup=False) as dag:

    printe = BashOperator(
        task_id="printe",
        bash_command='echo "- "{{ dag_run.conf["param1"] }} " xxx" {{ dag_run.conf["param2"] }}',
    )

    printe