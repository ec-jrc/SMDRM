ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.7-slim as builder
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

# build env variables
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy https_proxy=$https_proxy

ARG DEEPPAVLOV_HOME=/opt/deeppavlov
ARG DEEPPAVLOV_CONFIG=ner_ontonotes_bert_mult

# runtime env variables
ENV CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    DEEPPAVLOV_HOME=$DEEPPAVLOV_HOME \
    DEEPPAVLOV_CONFIG=$DEEPPAVLOV_CONFIG

# install build deps
RUN apt update \
    && apt install -y \
      curl \
      gcc \
      g++ \
      git; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --upgrade pip setuptools wheel; \
    useradd -ms /bin/bash -d $DEEPPAVLOV_HOME deeppavlov

# set the working directory
WORKDIR $DEEPPAVLOV_HOME

# deeppavlov uses the user home to install
# models and config into .deeppavlov/
VOLUME $DEEPPAVLOV_HOME/.deeppavlov

# copy source code, and download instructions
COPY download.py .
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && python -m deeppavlov install $DEEPPAVLOV_CONFIG; \
    HOME=$DEEPPAVLOV_HOME python download.py
COPY api.py .

# install package from source
RUN chown -R deeppavlov: $DEEPPAVLOV_HOME

# login as unpriviledged user as per Docker Best Practices
USER deeppavlov


# Development stage
FROM builder as dev
CMD python api.py --debug


# Testing stage
FROM builder as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]

