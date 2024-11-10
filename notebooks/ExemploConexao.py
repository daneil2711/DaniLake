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
    .config("spark.sql.warehouse.dir", "hdfs://hadoop:9000/users/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://hadoop:9083") \
    .config("spark.jars", "/usr/spark/jars/mssql-jdbc-6.2.2.jre8.jar") \
    .enableHiveSupport()

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark

# %% [markdown]
# ## Testando Conexão HDFS

# %%
#Criando diretorio
# !hdfs dfs -mkdir  hdfs://hadoop:9000//users/Teste

# %%
#movendo arquivos do local para o HDFS
# !hdfs dfs -put /notebooks/curva.csv  hdfs://hadoop:9000/users/Teste

# %%
#Listando diretorios/arquivos
# !hdfs dfs -ls  hdfs://hadoop:9000//users/Teste/

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
df = spark.read.csv('hdfs://hadoop:9000/users/Teste/curva.csv',header=True,sep=';')

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
jdbc_url = "jdbc:sqlserver://sqlserver:1433;databaseName=testeDani"
connection_properties = {
    "user": "SA",
    "password": "YourStrong!Passw0rd",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# df = spark.read.jdbc(url=jdbc_url, table="daniBoy", properties=connection_properties)
# df.show()


# %%
query_cliente = '''(
SELECT

PAR.CODPARC AS 'Cód Parceiro',
PAR.RAZAOSOCIAL AS 'Razão Social',
PAR.CGC_CPF AS CNPJ,
ISNULL (PAR.TELEFONE,'') AS Telefone,
isnull (par.fax,'') as Celular,
ISNULL (PAR.EMAIL,'') AS 'E-mail',
ISNULL (UFS.UF,'')AS UF,
ISNULL (CID.NOMECID,'') AS Cidade

FROM SANKHYA.TGFPAR PAR
JOIN SANKHYA.TSIEND END1 ON PAR.CODEND = END1.CODEND
JOIN SANKHYA.TSIBAI BAI ON PAR.CODBAI = BAI.CODBAI
JOIN SANKHYA.TSICID CID ON CID.CODCID = PAR.CODCID
JOIN SANKHYA.TSIUFS UFS ON UFS.CODUF = CID.UF

WHERE PAR.ATIVO = 'S'
AND PAR.CLIENTE = 'S'
AND CGC_CPF IS NOT NULL
AND PAR.CODPARC > 3
AND PAR.TIPPESSOA = 'J'
) as cliente
'''

# %%
connection_properties = {
    "user": "SA",
    "password": "YourStrong!Passw0rd",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

jdbc_url = "jdbc:sqlserver://sqlserver:1433;databaseName=SANKHYA_PARI"
df = spark.read.jdbc(url=jdbc_url,
table=query_cliente, properties=connection_properties)
df.show()

# %%
