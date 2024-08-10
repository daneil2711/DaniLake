from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.operators.papermill import PapermillOperator
from datetime import datetime
from datetime import date

delay = '{{ dag_run.conf["delay"] }}'
dt_start = date.today()
dt_stop = date.today()

with DAG("roda_gut2", 
         start_date=datetime(2021, 1, 1), 
         schedule="@daily", 
         catchup=False) as dag:

    # ingestao = PapermillOperator(
    #     task_id="ingestao",
    #     input_nb="/mnt/c/Users/danei/Desktop/Estudos/DataSus/ingestao.ipynb",
    #     output_nb="/mnt/c/Users/danei/Desktop/Estudos/DataSus/ingestao_out.ipynb",
    #     parameters=dict(dt_start = '2022-01-01',dt_stop = '2022-02-01')
    # )

    # transform = PapermillOperator(
    #     task_id="ingestao",
    #     input_nb="/mnt/c/Users/danei/Desktop/Estudos/DataSus/transform.ipynb",
    #     output_nb="/mnt/c/Users/danei/Desktop/Estudos/DataSus/transform_out.ipynb",
    #     parameters=dict(dt_start = '2022-01-01',dt_stop = '2022-02-01') --{{ dag_run.start_date }} 
    # )

    ingestion_raw = BashOperator(
        task_id="ingestion_raw",
        bash_command=f'papermill /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Raw/ingestao.ipynb /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Raw/ingestao_out.ipynb -p dt_start {dt_start} -p dt_stop {dt_stop} -p delay {delay}'
    )

    transforming_raw = BashOperator(
        task_id="transforming_raw",
        bash_command="papermill /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Raw/transform.ipynb /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Raw/transform_out.ipynb"
    )

    moveHDFS = BashOperator(
        task_id="moveHDFS",
        bash_command="python3 /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/scripts/MoveArquivos.py"
    )

    ingestion_bronze = BashOperator(
        task_id="ingestion_bronze",
        bash_command="papermill /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Bronze/ingestao.ipynb /mnt/c/Users/Daniel/Desktop/Estudos/DataSus/Bronze/ingestao_out.ipynb"
    )

    ingestion_raw >> transforming_raw >> moveHDFS >> ingestion_bronze