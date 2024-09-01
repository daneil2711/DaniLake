# Use a imagem oficial do SQL Server 2022 Developer
FROM mcr.microsoft.com/mssql/server:2022-latest

# Definir variáveis de ambiente
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong!Passw0rd

# Expor a porta do SQL Server
EXPOSE 1433

# Habilitar o SQL Server Agent
RUN /opt/mssql/bin/mssql-conf set sqlagent.enabled true

# Reiniciar o serviço SQL Server para aplicar a configuração
RUN /opt/mssql/bin/sqlservr --accept-eula & sleep 20 && pkill sqlservr

# Comando para iniciar o SQL Server
CMD ["/opt/mssql/bin/sqlservr"]
