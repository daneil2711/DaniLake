FROM openjdk:8-jdk-slim

#Vars hadoop
ENV HADOOP_VERSION 3.2.4
ENV HADOOP_HOME /usr/hadoop
ENV HADOOP_INSTALL $HADOOP_HOME
ENV HADOOP_MAPRED_HOME $HADOOP_HOME
ENV HADOOP_COMMON_HOME $HADOOP_HOME
ENV HADOOP_HDFS_HOME $HADOOP_HOME
ENV HADOOP_YARN_HOME $HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE $HADOOP_HOME/lib/native
ENV HADOOP_USER_CLASSPATH_FIRST true
ENV PATH $PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HADOOP_OPTS "-Djava.library.path=$HADOOP_HOME/lib/native"

ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER_URL=spark://spark-master:7077

#Vars Hive
ENV HIVE_VERSION 3.1.2
ENV HIVE_HOME /usr/hive
ENV HIVE_LIB /usr/hive/lib
ENV HIVE_CONF_DIR $HIVE_HOME/conf
ENV PATH $PATH:$HIVE_HOME/bin
ENV CLASSPATH $CLASSPATH:$HADOOP_HOME/lib/*:.
ENV CLASSPATH $CLASSPATH:$HIVE_HOME/lib/*:.

#Vars Derby
ENV DERBY_HOME /usr/derby
ENV PATH $PATH:$DERBY_HOME/bin

#Vars Spark
ENV SPARK_VERSION 3.4.3
ENV SPARK_HOME /usr/spark
ENV PATH $PATH:$SPARK_HOME/bin

USER root

#Instalação Hadoop
RUN apt-get update \
    && apt-get install -y ssh wget openssh-server\
    && wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
    && mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && mkdir /usr/hadoop/data \
    && mkdir /usr/hadoop/data/namenode \
    && mkdir /usr/hadoop/data/datanode \
    && chown -R root:root ${HADOOP_HOME} \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/environment

# Copia dos XMLs de conf
COPY configs/hadoop/*.xml ${HADOOP_HOME}/etc/hadoop/

#Configs SSH
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 640 ~/.ssh/authorized_keys

#Instalação Hive
RUN wget https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && tar -xzf apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && rm apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && mv apache-hive-${HIVE_VERSION}-bin ${HIVE_HOME} \
    && rm ${HIVE_HOME}/lib/guava-19.0.jar \
    && cp ${HADOOP_HOME}/share/hadoop/common/lib/guava-27.0-jre.jar ${HIVE_HOME}/lib/

#Arquivos de conf hive
COPY configs/hive/hive-site.xml ${HIVE_HOME}/conf
COPY configs/hive/hive-env.sh ${HIVE_HOME}/conf
COPY configs/hive/hive-schema-3.1.0.derby.sql ${HIVE_HOME}/scripts/metastore/upgrade/derby

#Instalação Derby
RUN wget https://archive.apache.org/dist/db/derby/db-derby-10.14.2.0/db-derby-10.14.2.0-bin.tar.gz \
    && tar -xzf db-derby-10.14.2.0-bin.tar.gz \
    && rm db-derby-10.14.2.0-bin.tar.gz \
    && mv db-derby-10.14.2.0-bin ${DERBY_HOME} \
    && cp -r ${DERBY_HOME}/lib /${HADOOP_HOME}/lib

#Instalação SPARK
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
&& tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz \
&& rm spark-${SPARK_VERSION}-bin-hadoop3.tgz \
&& mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} 

#Arquivos de conf hive
COPY configs/spark/*.xml ${SPARK_HOME}/conf

#Instalação Jupyter
COPY configs/jupyter/requirements.txt /
RUN apt install -y python3 pip \
    && pip install jupyterlab \
    && mkdir /usr/notebooks \
    && pip install -r requirements.txt

#Instalação R
RUN apt-get update 
RUN apt install software-properties-common dirmngr -y 
#Necessario para instalar o factoextra (Kmeans) cmake e tydeverse (todo o resto) no R
RUN apt install cmake libssl-dev libfontconfig1-dev libcurl4-openssl-dev libxml2-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev -y

COPY configs/scripts/gpg.sh /
#GPG falha ao adicionar a chave na primeira tentantiva (aparentemente cria um diretório e arquivo necessário para adicionar a chave)
# Fiz o script pensando na falha para funcionar no comando abaixo
RUN sh gpg.sh

RUN gpg --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' 
RUN gpg --armor --export '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' | tee /etc/apt/trusted.gpg.d/cran_debian_key.asc \
    && add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian bullseye-cran40/' \
    && apt-get update \
    && apt install r-base r-base-dev -y 

RUN R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel', 'rms', 'ROCR'), type = 'source')" \
    && R -e "IRkernel::installspec(user = FALSE)"

#scripts spark
COPY configs/scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/start-master.sh /usr/local/bin/start-worker.sh /usr/local/bin/bootstrap.sh
    
#expose portas
EXPOSE 9870 8088 9000 8042 9864 8888 10000 10001 11002 7077 8080 8081

#bootstrap
# COPY configs/scripts /
# ENTRYPOINT ["/bin/bash", "bootstrap.sh"]

