# Use the official SQL Server 2022 Developer image
FROM mcr.microsoft.com/mssql/server:2022-latest

# Set environment variables
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong!Passw0rd

# Expose the SQL Server port
EXPOSE 1433

# Optional: Run a custom script or command here
# COPY your-script.sql /scripts/
# RUN /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -i /scripts/your-script.sql

# Start SQL Server
CMD ["/opt/mssql/bin/sqlservr"]
