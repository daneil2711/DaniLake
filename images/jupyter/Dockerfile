FROM ubuntu:20.04

#Vars pra pular o interativo da instalação do R
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

#Instalação Jupyter
COPY configs/ /
RUN apt-get update \
    && apt install -y python3-pip\
    && pip install jupyterlab \
    && mkdir /usr/notebooks 
    # && pip install -r requirements.txt

RUN apt install software-properties-common dirmngr wget -y 

RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc   
RUN add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# #Instalação R 
RUN apt-get update \
    && apt-get install r-base r-base-dev -y --fix-missing \
    && apt-get install libzmq3-dev libcurl4-openssl-dev libssl-dev jupyter-core jupyter-client -y --fix-missing
RUN R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel'), type = 'source')" \
    && R -e "IRkernel::installspec(user = FALSE)"

EXPOSE 8888

ENTRYPOINT ["/bin/bash", "bootstrap.sh"]
