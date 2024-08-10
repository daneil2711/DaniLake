from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import subprocess

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

def run_spark_script():
    # Caminho para o script .py que você deseja executar
    script_path = '/opt/airflow/dags/sql.py'
    
    # Comando para executar o script usando o Python instalado no container
    subprocess.run(['python3', script_path], check=True)

# Definindo a DAG
with DAG(
    'spark_python_operator_example',
    default_args=default_args,
    description='Executa um script PySpark via PythonOperator',
    schedule_interval=None,
) as dag:

    # Operador PythonOperator
    run_spark_task = PythonOperator(
        task_id='run_spark_task',
        python_callable=run_spark_script,
    )

    run_spark_task

