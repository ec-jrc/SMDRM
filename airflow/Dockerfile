ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/apache/airflow:2.2.3 as builder

LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ARG AIRFLOW_UID

# I5 Network proxy url
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy https_proxy=$https_proxy

# extend image
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_OP_PATH="/home/airflow/.local/lib/python3.7/site-packages/airflow/providers/docker/operators/docker.py"

USER airflow
# override docker operator with custom version
COPY --chown=airflow:0 custom_ops/docker.py $DOCKER_OP_PATH

# copy source code
COPY --chown=airflow:0 dags dags
COPY --chown=airflow:0 tests tests

# update pip and install pytest
RUN python -m pip install --upgrade pip pytest

