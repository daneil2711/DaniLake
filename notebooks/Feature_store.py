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
import pyspark.sql.functions as F
import pandas as pd

from feast import Entity, FeatureView, Field
from feast.types import Float32, Int64, UnixTimestamp
from feast import FeatureStore
from feast.infra.offline_stores.contrib.spark_offline_store.spark_source import(
    SparkSource,
)
builder = pyspark.sql.SparkSession.builder.appName("Feast") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.executor.cores", "2") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.cores", "2") \
    .config("spark.driver.memory", "2g") \
    .config("spark.cores.max", "4") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .enableHiveSupport()

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark

# %%
spark.sql('CREATE DATABASE IF NOT EXISTS teste_feature')

# %%
data = [
    (1, "user_1", 0.5),
    (2, "user_2", 0.7),
    (3, "user_3", 0.8)
]

df = spark.createDataFrame(data, ["id", "name", "feature_value"])
df = df.withColumn("event_time", F.lit('2022-01-01'))
# Salva como uma tabela Delta
df.write.format("delta").mode("overwrite").option("mergeSchema","true").saveAsTable("teste_feature.feature_table")

# %%
# Inicialize o FeatureStore apontando para o arquivo feature_store.yaml
store = FeatureStore(repo_path="/usr/notebooks/feast/")

# %%
# Define a entidade (entidade básica para nossas features)
user_entity = Entity(name="user", join_keys=["id"])

# Define a origem dos dados (de onde as features serão carregadas)
source = SparkSource(
    table='teste_feature.feature_table',
    name='TestFeature',
    timestamp_field="event_time"
)

# Define as features
feature_view = FeatureView(
    name="user_features",
    entities=[user_entity],
    ttl=None,
    schema=[
        Field(name="id", dtype=Int64),
        Field(name="feature_value", dtype=Float32),
        Field(name="event_time", dtype=UnixTimestamp)
    ],
    online=False,
    source=source
)

# Inicializa o FeatureStore
store = FeatureStore(repo_path="/usr/notebooks/feast")

# Registra a feature view no Feast
store.apply([feature_view])

# %%
# Recupera as features registradas
features = store.get_feature_view("user_features")

print("Features registradas:", features)

# %%
# Cria um DataFrame com as entidades e a coluna event_timestamp
entity_df = pd.DataFrame({
    "id": [1, 2, 3],
    "event_timestamp": pd.to_datetime(['2022-01-01', '2022-01-01', '2022-01-01'], format='%Y-%m-%d')
})

# Tenta obter as features para um determinado conjunto de entidades
features = store.get_historical_features(
    features=["user_features:feature_value"],
    entity_df=entity_df
).to_df()

print(features)

# %%
spark.sql('drop DATABASE teste_feature cascade')
