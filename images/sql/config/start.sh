#!/bin/bash

# Monta o OneDrive usando rclone
rclone mount onedrive:/MBA /mnt/onedrive --vfs-cache-mode writes --allow-other &

# Inicia o SSH e o SQL Server
service ssh start
/opt/mssql/bin/sqlservr