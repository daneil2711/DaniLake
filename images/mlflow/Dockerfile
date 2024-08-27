# Usando a imagem base do Python
FROM python:3.9-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Instalando as dependências necessárias
RUN pip install mlflow

# Expondo a porta em que o MLflow será executado
EXPOSE 5000

# Comando para iniciar o MLflow UI
CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"]
