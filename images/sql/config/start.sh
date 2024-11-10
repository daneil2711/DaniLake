#!/bin/bash

# Monta o OneDrive usando rclone
rclone mount onedrive:/SQL/Query /mnt/onedrive/SQL --vfs-cache-mode writes --allow-other &
rclone mount onedrive:/MBA /mnt/onedrive/MBA --vfs-cache-mode writes --allow-other &

# Inicia o SSH e o SQL Server
service ssh start
/opt/mssql/bin/sqlservr