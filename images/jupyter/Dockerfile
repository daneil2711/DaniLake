FROM python

COPY configs/requirements.txt /
#Instalação Jupyter
RUN apt-get update \
    && pip install jupyterlab \
    && mkdir notebooks \
    && pip install -r requirements.txt

#Instalação R
RUN apt-get install r-base r-base-dev -y --fix-missing \
    && apt-get install libzmq3-dev libcurl4-openssl-dev libssl-dev jupyter-core jupyter-client -y 
RUN R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel'), type = 'source')" \
    && R -e "IRkernel::installspec(user = FALSE)"

EXPOSE 8888
COPY configs/scripts /

ENTRYPOINT ["/bin/bash", "bootstrap.sh"]
