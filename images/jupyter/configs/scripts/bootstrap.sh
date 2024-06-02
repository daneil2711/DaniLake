#!/bin/bash

#iniciando o jupyter
jupyter-lab --NotebookApp.token='' --ip='0.0.0.0' --port=8888 --no-browser --allow-root

while :; do sleep 2073600; done