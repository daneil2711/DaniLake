FROM openjdk:8-jdk-slim

ENV HADOOP_VERSION 3.2.4
ENV HADOOP_HOME /usr/hadoop
ENV HADOOP_INSTALL $HADOOP_HOME
ENV HADOOP_MAPRED_HOME $HADOOP_HOME
ENV HADOOP_COMMON_HOME $HADOOP_HOME
ENV HADOOP_HDFS_HOME $HADOOP_HOME
ENV HADOOP_YARN_HOME $HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE $HADOOP_HOME/lib/native
ENV PATH $PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HADOOP_OPTS "-Djava.library.path=$HADOOP_HOME/lib/native"

USER root

#Instalação Hadoop
RUN apt-get update \
    && apt-get install -y ssh wget openssh-server\
    && wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
    && mv hadoop-${HADOOP_VERSION} /usr/hadoop \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && mkdir /usr/hadoop/data \
    && mkdir /usr/hadoop/data/namenode \
    && mkdir /usr/hadoop/data/datanode \
    && chown -R root:root ${HADOOP_HOME} \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/environment

#Configs SSH
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 640 ~/.ssh/authorized_keys

COPY configs/jupyter/requirements.txt /
#Instalação Jupyter
RUN apt install -y python3 pip \
    && pip install jupyterlab \
    && mkdir /usr/notebooks \
    && pip install -r requirements.txt

#Instalação R
RUN apt-get install r-base r-base-dev -y --fix-missing \
    && apt-get install libzmq3-dev libcurl4-openssl-dev libssl-dev jupyter-core jupyter-client -y 
RUN R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel'), type = 'source')" \
    && R -e "IRkernel::installspec(user = FALSE)"

# Copia dos XMLs de conf e script pra rodar os comandos
COPY configs/hadoop/*.xml ${HADOOP_HOME}/etc/hadoop/
COPY configs/scripts /

EXPOSE 9000 22 8888

ENTRYPOINT ["/bin/bash", "bootstrap.sh"]

