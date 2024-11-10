# Base image
FROM mcr.microsoft.com/mssql/server:2022-latest

USER root

# Install OpenSSH Server, curl, and fuse
RUN apt-get update && \
    apt-get install -y openssh-server curl fuse3 && \
    mkdir /var/run/sshd

# Set environment variables (SA_PASSWORD should be set at runtime for security)
ENV ACCEPT_EULA=Y

# Copy SQL Server configuration
COPY config/mssql.conf /var/opt/mssql

# Baixa e instala o rclone
RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.deb && \
    dpkg -i rclone-current-linux-amd64.deb && \
    rm rclone-current-linux-amd64.deb

# Copia o arquivo de configuração rclone.conf que contém a autenticação do OneDrive
COPY config/rclone.conf /root/.config/rclone/rclone.conf

# Cria o ponto de montagem para o OneDrive
RUN mkdir -p /mnt/onedrive

# Expose ports for SQL Server and SSH
EXPOSE 1433 22 53682

# Configure SSH
RUN echo 'root:YourRootPassword' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Script de inicialização para montar o OneDrive e iniciar os serviços
COPY config/start.sh /start.sh
RUN chmod +x /start.sh

# Define o comando para rodar o script de inicialização
CMD ["/start.sh"]
