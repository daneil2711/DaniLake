#!/bin/bash

#Validação namenode
HDFS_METADATA_DIR=$HADOOP_HOME/data/namenode/

if [ "$(ls -A $HDFS_METADATA_DIR)" ]; then
    echo "NameNode já está formatado."
else
    echo "Formatando o NameNode..."
    hdfs namenode -format
fi

#Start SSH
/etc/init.d/ssh start

export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
export SPARK_MASTER_HOST=spark-master
export SPARK_MASTER_URL=spark://spark-master:7077

# Startando hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

sleep 10
#Inclusão Users
hdfs dfs -mkdir /users/
hdfs dfs -mkdir /users/Daniel
hdfs dfs -chown -R Daniel:root /users/Daniel

# # Startando hive
nohup startNetworkServer &
sleep 5
nohup schematool -dbType derby -initSchema &
sleep 5
nohup hive --service metastore &
sleep 5
nohup hive --service hiveserver2 &
sleep 5

#iniciando jupyter
cd /usr/notebooks
nohup jupyter-lab --NotebookApp.token='' --NotebookApp.disable_check_xsrf=True --ip='0.0.0.0' --port=8888 --no-browser --allow-root &
sleep 5

# Função para criar o usuário administrador
create_admin_user() {
    airflow users create \
        --username admin \
        --password admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com
}

# Espera pelo banco de dados estar disponível
until airflow db check; do
    echo "Waiting for database..."
    sleep 5
done

# Inicializa o banco de dados do Airflow (se necessário)
airflow db init

# Verifica se o usuário administrador já existe
admin_exists=$(airflow users list | grep admin)

if [ -z "$admin_exists" ]; then
    echo "Creating admin user..."
    create_admin_user
else
    echo "Admin user already exists"
fi
sleep 5

airflow scheduler &
sleep 5
#Iniciando airflow
nohup airflow webserver -p 8099 &
sleep 10
## Ajustando spark conf
# URL da API do Airflow (ajuste conforme necessário)
AIRFLOW_API_URL="http://localhost:8099/api/v1/connections"

# ID da conexão que queremos configurar
CONNECTION_ID="spark_default"

# JSON com os dados da conexão
CONNECTION_JSON=$(cat <<EOF
{
  "connection_id": "$CONNECTION_ID",
  "conn_type": "spark",
  "host": "spark://spark-master",
  "port": 7077,
  "extra": "{\"queue\": \"root.default\", \"deploy-mode\": \"client\"}"
}
EOF
)

# Delete e depois Post do conf (n consegui usar o PATCH)
curl -X DELETE "$AIRFLOW_API_URL/$CONNECTION_ID" \
  -u "admin:admin"

response=$(curl -X POST $AIRFLOW_API_URL \
  -H "Content-Type: application/json" \
  -u "admin:admin" \
  -d "$CONNECTION_JSON")

echo "Resposta da API: $response"

while :; do sleep 2073600; done