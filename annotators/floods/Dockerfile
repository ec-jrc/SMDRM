# syntax=docker/dockerfile:1
ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.8-slim

LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

# build env varibles
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy \
    https_proxy=$https_proxy \
    CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive

# install build deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        unzip \
        locales && \
    printf '%s\n%s\n' 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
	rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache

# runtime env variables
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# create non priviledged user
RUN useradd -m user
USER 1000

# prepare environment
RUN cd /home/user && \
        python -m venv venv && \
        venv/bin/pip install -U pip setuptools wheel && \
        mkdir -p models
ENV PATH=/home/user/venv/bin:$PATH
WORKDIR /home/user

# install requirements
COPY --chown=1000:1000 requirements.txt  .
RUN pip install -r requirements.txt

# copy souce code
COPY --chown=1000:1000 start.sh .
COPY --chown=1000:1000 wsgi.py .
COPY --chown=1000:1000 app app
COPY --chown=1000:1000 tests tests

# runtime execution
CMD ["./start.sh"]

