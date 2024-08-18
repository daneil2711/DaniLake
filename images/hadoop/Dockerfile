# Stage 1: Base com dependências principais
FROM openjdk:8-jdk-slim AS base

# Definição de variáveis
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

# Instalando Hadoop
RUN apt-get update && apt-get install -y ssh wget curl openssh-server \
    && wget "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz \
    && mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && mkdir /usr/hadoop/data \
    && mkdir /usr/hadoop/data/namenode \
    && mkdir /usr/hadoop/data/datanode \
    && chown -R root:root ${HADOOP_HOME} \
    && ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 640 ~/.ssh/authorized_keys \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/environment

# Stage 2: Instalação do Hive e Derby
FROM base AS hive_derby

# Definição de variáveis Hive e Derby
ENV HIVE_VERSION 3.1.2
ENV HIVE_HOME /usr/hive
ENV HIVE_LIB /usr/hive/lib
ENV HIVE_CONF_DIR $HIVE_HOME/conf
ENV DERBY_HOME /usr/derby
ENV PATH $PATH:$HIVE_HOME/bin:$DERBY_HOME/bin
ENV CLASSPATH $CLASSPATH:$HADOOP_HOME/lib/*:$HIVE_HOME/lib/*:.

# Instalando Hive e Derby
RUN wget https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && tar -xzf apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && mv apache-hive-${HIVE_VERSION}-bin ${HIVE_HOME} \
    && rm apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && rm ${HIVE_HOME}/lib/guava-19.0.jar \
    && cp ${HADOOP_HOME}/share/hadoop/common/lib/guava-27.0-jre.jar ${HIVE_HOME}/lib/ \
    && wget https://archive.apache.org/dist/db/derby/db-derby-10.14.2.0/db-derby-10.14.2.0-bin.tar.gz \
    && tar -xzf db-derby-10.14.2.0-bin.tar.gz \
    && mv db-derby-10.14.2.0-bin ${DERBY_HOME} \
    && rm db-derby-10.14.2.0-bin.tar.gz \
    && cp -r ${DERBY_HOME}/lib /${HADOOP_HOME}/lib

# Stage 3: Instalação do Spark e airflow Jupyter
FROM hive_derby AS spark_jupyter

ENV SPARK_VERSION 3.4.3
ENV SPARK_HOME /usr/spark
ENV PATH $PATH:$SPARK_HOME/bin
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_URL spark://spark-master:7077
# Vars Airflow
ENV AIRFLOW_HOME /opt/airflow
ENV AIRFLOW__CORE__TEST_CONNECTION Enabled
ENV AIRFLOW__WEBSERVER__WEB_SERVER_PORT 8099
ENV AIRFLOW__CORE__LOAD_EXAMPLES False 
ENV AIRFLOW__CLI__ENDPOINT_URL http://localhost:8099
ENV AIRFLOW__API__ENABLE_EXPERIMENTAL_API True
ENV AIRFLOW__API__AUTH_BACKENDS airflow.api.auth.backend.basic_auth

# Instalando Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz \
#Instalação do JAR para conexão com SQL Server -- peguei a versão 6.2 por questão de compatibilidade com o Java8
# https://learn.microsoft.com/en-us/sql/connect/jdbc/microsoft-jdbc-driver-for-sql-server-support-matrix?view=sql-server-ver15#java-and-jdbc-specification-support
# Passei o link da versão 6.2 hardcode
    && wget -O mssql-jdbc.tar.gz https://go.microsoft.com/fwlink/?linkid=2122615 \
    && tar -xzf mssql-jdbc.tar.gz --one-top-level=mssql-jdbc --strip-components=1 \
    && cp -r mssql-jdbc/enu/*jar ${SPARK_HOME}/jars/ \
    && rm mssql-jdbc.tar.gz \
    && rm -rf mssql-jdbc 

# Instalando Jupyter
RUN apt-get install -y python3 pip \
    && pip install jupyterlab \
    && mkdir /usr/notebooks

# Instalando Airflow
RUN pip install apache-airflow==2.8.1 \
&& pip uninstall apache-airflow-providers-fab -y

# Stage 4: Instalação do Airflow, R e configuração final
FROM spark_jupyter AS final

#Necessario para instalar o factoextra (Kmeans) cmake e tydeverse (todo o resto) no R
RUN apt-get update \
    && apt install -y software-properties-common dirmngr cmake libssl-dev libfontconfig1-dev libcurl4-openssl-dev libxml2-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev

#GPG falha ao adicionar a chave na primeira tentantiva (aparentemente cria um diretório e arquivo necessário para adicionar a chave)
# Fiz o script pensando na falha para funcionar no comando abaixo
COPY configs/scripts/gpg.sh /
RUN sh gpg.sh \
    && gpg --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' \
    && gpg --armor --export '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7' | tee /etc/apt/trusted.gpg.d/cran_debian_key.asc \
    && add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian bullseye-cran40/' \
    && apt-get update \
    && apt install r-base r-base-dev -y 
    
#Lib R
RUN R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel', 'rms', 'ROCR','GGally','car','igraph','arules','arulesViz','urca','forecast','tidyverse','factoextra','Information'), type = 'source')" \
    && R -e "IRkernel::installspec(user = FALSE)"

# Instalando bibliotecas Python do Jupyter
COPY configs/jupyter/requirements.txt /
RUN pip install -r requirements.txt

# Copia dos XMLs de conf
COPY configs/hadoop/*.xml ${HADOOP_HOME}/etc/hadoop/
# Copia das configurações Hive
COPY configs/hive/hive-site.xml ${HIVE_HOME}/conf
COPY configs/hive/hive-env.sh ${HIVE_HOME}/conf
COPY configs/hive/hive-schema-3.1.0.derby.sql ${HIVE_HOME}/scripts/metastore/upgrade/derby
# Copia das configurações Spark
COPY configs/spark/*.xml ${SPARK_HOME}/conf/

# Copiando e configurando os scripts do Spark
COPY configs/scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/start-master.sh /usr/local/bin/start-worker.sh /usr/local/bin/bootstrap.sh 

# Expose portas
EXPOSE 9870 8088 9000 8042 9864 8888 10000 10001 11002 7077 8080 8081 8099 4040