FROM openjdk:8-jdk-slim

ENV HADOOP_VERSION 3.2.4
ENV HADOOP_HOME /usr/hadoop

USER root

#Instalação Hadoop
RUN apt-get update \
    && apt-get install -y ssh pdsh wget openssh-server\
    && wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
    && mv hadoop-${HADOOP_VERSION} /usr/hadoop \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && chown -R root:root ${HADOOP_HOME} \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/environment

# Copia dos XMLs de conf e script pra rodar os comandos
COPY configs/hadoop/*.xml ${HADOOP_HOME}/etc/hadoop/
COPY configs/scripts /

#Configs SSH
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 640 ~/.ssh/authorized_keys

EXPOSE 9000 22 9870

ENTRYPOINT ["/bin/bash", "bootstrap.sh"]