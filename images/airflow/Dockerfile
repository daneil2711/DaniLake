FROM apache/airflow:2.8.1-python3.10

ENV AIRFLOW_HOME=/opt/airflow

# Instale pacotes adicionais do Python, se necessário
COPY configs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

COPY configs/entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
