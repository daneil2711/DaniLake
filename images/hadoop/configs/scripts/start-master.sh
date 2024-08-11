#!/bin/bash

# start-master.sh

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master --host $SPARK_MASTER_HOST --port 7077
