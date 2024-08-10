#!/bin/bash

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

airflow scheduler &

exec airflow webserver -p 8080
