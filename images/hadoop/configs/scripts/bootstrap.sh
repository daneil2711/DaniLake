#!/bin/bash

/etc/init.d/ssh start
hdfs namenode -format

export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root

# Startando serviços
$HADOOP_HOME/sbin/start-dfs.sh

#Inclusão Users
hdfs dfs -mkdir -p /user/Daniel
hdfs dfs -chown -R Daniel:root /user/Daniel

while :; do sleep 2073600; done