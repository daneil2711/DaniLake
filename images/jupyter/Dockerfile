FROM condaforge/mambaforge:23.3.1-0

# Instalar dependências adicionais do sistema, incluindo o Java 8 sem interação
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y curl vim-tiny openjdk-8-jdk tzdata

# Configurar o JAVA_HOME para o Java 8
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copiar os arquivos de ambiente
COPY env/myenv.yml /tmp/env.yml

# Configurar o ambiente conda
RUN mamba env create -f /tmp/env.yml \
    && conda clean -afy

# Ativar o ambiente conda e instalar pyspark e delta-spark primeiro
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv \
    && pip install pyspark==3.4.3 \
    && pip install delta-spark==2.4.0"

# Config jupyter pra utilizar notebook como .py
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv && jupyter-lab --generate-config"
COPY env/jupyter_lab_config.py /root/.jupyter/

# Copiar o requirements.txt e instalar as dependências extras via pip
COPY env/requirements.txt /tmp/requirements.txt
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate myenv \
    && pip install -r /tmp/requirements.txt"



ENV HADOOP_VERSION 3.2.4
RUN apt-get update && apt-get install -y ssh wget curl openssh-server maven\
&& wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
&& tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
&& mv hadoop-${HADOOP_VERSION} /usr/local/hadoop \
&& rm hadoop-${HADOOP_VERSION}.tar.gz 

ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH:$JAVA_HOME/bin

ENV HDFS_NAMENODE_URI=hdfs://hadoop:9000

# Expor a porta do JupyterLab
EXPOSE 8888

# Criar um ponto de trabalho
WORKDIR /notebooks

#Script inicial
COPY env/start.sh  /