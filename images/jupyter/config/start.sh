#!/usr/bin/bash

# Monta o OneDrive usando rclone
rclone mount onedrive:/MBA /notebooks/MBA --vfs-cache-mode writes --allow-other &
rclone mount onedrive:/SQL/Query /notebooks/SQL --vfs-cache-mode writes --allow-other &

umask 007
source /opt/conda/etc/profile.d/conda.sh && conda activate myenv

echo "Iniciando Jupyter....."
#iniciando jupyter
cd /notebooks

jupyter-lab --NotebookApp.token='' --NotebookApp.disable_check_xsrf=True --ip='0.0.0.0' --port=8888 --no-browser --allow-root
sleep 5
while :; do sleep 2073600; done