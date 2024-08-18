# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pyspark
from delta import *

builder = pyspark.sql.SparkSession.builder.appName("Jupyter") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.executor.cores", "2") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.cores", "2") \
    .config("spark.driver.memory", "2g") \
    .config("spark.cores.max", "4") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .enableHiveSupport()

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark

# %% [markdown]
# ## Testando Conexão HDFS

# %%
#Criando diretorio
# !hdfs dfs -mkdir /users/Teste

# %%
#movendo arquivos do local para o HDFS
# !hdfs dfs -put /usr/notebooks/curva.csv /users/Teste

# %%
#Listando diretorios/arquivos
# !hdfs dfs -ls /users/Teste/

# %% [markdown]
# ## Testando Hive

# %%
spark.sql('CREATE DATABASE IF NOT EXISTS teste')

# %%
spark.sql('show databases').show()

# %% [markdown]
# ## Testando Spark

# %%
spark.range(10).show()

# %%
#Lendo arquivos do HDFS
df = spark.read.csv('/users/Teste/curva.csv',header=True,sep=';')

df.show()

# %%
#salvando tabela delta
df.write.format("delta").mode("overwrite").saveAsTable('teste.curva')

# %%
#Verificando resultados
spark.sql("select * from teste.curva").show()

# %% [markdown]
# ## Testando SQL Server

# %%
# jdbc_url = "jdbc:sqlserver://sqlserver:1433;databaseName=testeDani"
# connection_properties = {
#     "user": "SA",
#     "password": "YourStrong!Passw0rd",
#     "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
# }

# df = spark.read.jdbc(url=jdbc_url, table="daniBoy", properties=connection_properties)
# df.show()

