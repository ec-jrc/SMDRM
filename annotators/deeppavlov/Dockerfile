ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.7-slim as builder

LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ENV CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive

# set the working directory
WORKDIR /DeepPavlov

# install build deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        locales && \
    printf '%s\n%s\n' 'en_US.UTF-8 UTF-8' 'ru_RU.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
	rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache && \
    useradd -s /bin/bash -d /DeepPavlov -M user && \
    chown -R user:0 /DeepPavlov

# runtime env variables
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# make virtual env
USER user
RUN python -m venv ./venv
# add venv to PATH
ENV PATH=/DeepPavlov/venv/bin:$PATH
# upgrade pip base
RUN pip install --upgrade pip setuptools wheel

# assign user permissions
# ensure successful pip install
USER root
RUN chown -R user:0 /DeepPavlov

# install python dependencies
USER user
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY --chown=user:0 api.py start.sh ./
ENV CONFIG=ner_ontonotes_bert_mult
RUN python -m deeppavlov install $CONFIG


## Development stage
FROM builder as dev
CMD ["./start.sh"]


# Testing stage
FROM builder as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]


FROM builder as stg

# build env variables
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy https_proxy=$https_proxy

