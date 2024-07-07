#!/bin/bash

# Tentar adicionar a chave usando gpg --keyserver
gpg --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'

# Verificar o código de saída do comando gpg
if [ $? -ne 0 ]; then
  echo "Falha ao adicionar a chave. Executando ação alternativa."
  # Ação alternativa em caso de falha
  # Coloque aqui o que você deseja fazer em caso de falha
  # Por exemplo, registrar um erro, tentar outro servidor, etc.
else
  echo "Chave adicionada com sucesso."
fi
gpg --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
