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
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from feature_engine.encoding import OneHotEncoder
import shap
from sklearn.linear_model import LinearRegression

# %%
# Carregar a base de dados
data = pd.read_csv('../data/supermarket_sales.csv')  # Substitua pelo caminho da sua base
data.dtypes

# %%
# Dividir entre variáveis preditoras e variável resposta
X = data.drop(['Time','Date','Invoice ID'], axis=1)  # Substitua 'variavel_resposta' pelo nome da sua variável alvo
y = data['Quantity']

# %%
# Identificar variáveis categóricas e aplicar One-Hot Encoding usando feature-engine
encoder = OneHotEncoder(drop_last=True)  # drop_last=True para evitar multicolinearidade
X_encoded = encoder.fit_transform(X)

# %%
# Dividir em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# %%
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# %%
modelo

# %%
# Treinar o modelo
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)


# %%
# Usando SHAP para explicar a importância das variáveis
explainer = shap.Explainer(modelo, X_train)
shap_values = explainer(X_train)
# Plotar importância das variáveis
shap.summary_plot(shap_values, X_train)

# %%
dados_faturamento = pd.read_csv( "../data/Faturamento.txt",sep= "\t")
dados_faturamento

# %%
# Dividir entre variáveis preditoras e variável resposta
X = dados_faturamento.drop(['COD_PRODUTO'], axis=1)  # Substitua 'variavel_resposta' pelo nome da sua variável alvo
y = dados_faturamento['FATURAMENTO']

# %%
# Dividir em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# %%
# Usando SHAP para explicar a importância das variáveis
explainer = shap.Explainer(modelo, X_train)
shap_values = explainer(X_train)
# Plotar importância das variáveis
shap.plots.scatter(shap_values[:, 0])

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar a base de dados
data = pd.read_csv('../data/supermarket_sales.csv')
data = data.drop(['Time','Date','Invoice ID'], axis=1)

# Verificar estatísticas descritivas
print("Estatísticas descritivas:")
print(data.describe())

# Verificar valores ausentes
print("\nValores ausentes por coluna:")
print(data.isnull().sum())

# Visualizar a distribuição de variáveis numéricas
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numerical_columns].hist(bins=15, figsize=(15, 10), layout=(3, 3))
plt.suptitle('Distribuição das Variáveis Numéricas')
plt.show()

# Visualizar a distribuição de variáveis categóricas
categorical_columns = data.select_dtypes(include=['object']).columns

for col in categorical_columns:
    plt.figure(figsize=(10, 5))
    sns.countplot(data[col], order=data[col].value_counts().index)
    plt.title(f'Distribuição de {col}')
    plt.xticks(rotation=45)
    plt.show()

# Matriz de correlação
plt.figure(figsize=(12, 8))
correlation_matrix = data[numerical_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matriz de Correlação')
plt.show()

# Identificar possíveis outliers usando boxplots
for col in numerical_columns:
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data[col])
    plt.title(f'Outliers em {col}')
    plt.show()

