FROM apache/airflow:2.8.1-python3.10

ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__TEST_CONNECTION=Enabled
ENV AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8099

# Instale pacotes adicionais do Python, se necessário
COPY configs/requirements.txt .
RUN pip install -r requirements.txt 

EXPOSE 8099

COPY configs/entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
