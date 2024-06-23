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

# Startando hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# Startando hive
schematool -dbType derby -initSchema
nohup hive --service metastore > metastore.log 2>&1 &


#Inclusão Users
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/Daniel
# hdfs dfs -mkdir /user/hive/warehouse

# hdfs dfs -chown g+w /user
# hdfs dfs -chown g+w x/user
hdfs dfs -chown -R Daniel:root /user/Daniel

#iniciando jupyter
nohup jupyter-lab --NotebookApp.token='' --ip='0.0.0.0' --port=8888 --no-browser --allow-root &
while :; do sleep 2073600; done