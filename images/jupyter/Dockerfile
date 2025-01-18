FROM condaforge/mambaforge:23.3.1-0

# Instalar dependências adicionais do sistema, incluindo o Java 8 sem interação
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y curl vim-tiny openjdk-8-jdk tzdata

# Configurar o JAVA_HOME para o Java 8
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copiar os arquivos de ambiente
COPY config/myenv.yml /tmp/env.yml

# Configurar o ambiente conda
RUN mamba env create -f /tmp/env.yml \
    && conda clean -afy

# Ativar o ambiente conda e instalar pyspark e delta-spark primeiro
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv \
    && pip install pyspark==3.4.3 \
    && pip install delta-spark==2.4.0"

#Istalação hadoop
ENV HADOOP_VERSION 3.2.4
RUN apt-get update && apt-get install -y ssh wget openssh-server maven\
&& wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
&& tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
&& mv hadoop-${HADOOP_VERSION} /usr/local/hadoop \
&& rm hadoop-${HADOOP_VERSION}.tar.gz 

ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH:$JAVA_HOME/bin

ENV HDFS_NAMENODE_URI=hdfs://hadoop:9000

RUN pip install --upgrade pip setuptools

# Copiar o requirements.txt e instalar as dependências extras via pip
COPY config/requirements.txt /tmp/requirements.txt
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv \
    && pip install -r /tmp/requirements.txt --cache-dir=/root/.cache/pip"

# Install fuse e Rclone
RUN apt-get update && \
    apt-get install -y fuse3

RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.deb && \
    dpkg -i rclone-current-linux-amd64.deb && \
    rm rclone-current-linux-amd64.deb

# Copia o arquivo de configuração rclone.conf que contém a autenticação do OneDrive
COPY config/rclone.conf /root/.config/rclone/rclone.conf

# Config jupyter pra utilizar notebook como .py
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv && jupyter-lab --generate-config"
COPY config/jupyter_lab_config.py /root/.jupyter/

# Criando diretorios
RUN mkdir -p /usr/notebooks && \
    mkdir -p /usr/notebooks/MBA && \
    mkdir -p /usr/notebooks/SQL

ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4
ENV NUMEXPR_NUM_THREADS=4

# Expor a porta do JupyterLab
EXPOSE 8888

#Script inicial
COPY config/start.sh  /