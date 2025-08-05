FROM apache/airflow:2.3.2
USER root
RUN apt-get update && apt-get install -y mc
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt
