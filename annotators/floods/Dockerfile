ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.8-slim as builder
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

# build env varibles
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy https_proxy=$https_proxy

ARG FLOODS_HOME=/opt/floods
ARG MODELS_DIR=$FLOODS_HOME/models

# runtime env variavles
ENV CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    FLOODS_HOME=$FLOODS_HOME \
    MODELS_DIR=$MODELS_DIR \
    PATH=$PATH:$FLOODS_HOME/.local/bin

# install build deps
RUN apt update \
    && apt install -y \
      curl \
      git; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --upgrade pip setuptools wheel; \
    useradd -ms /bin/bash -d $FLOODS_HOME floods

# set the working directory
WORKDIR $FLOODS_HOME

# Floods model download models into models/ inside the FLOODS_HOME
# attach a volume to cache the created artifacts to reuse it
VOLUME $MODELS_DIR

# install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# install models
COPY download.sh .
RUN bash download.sh $MODELS_DIR

# copy souce code
COPY wsgi.py .
COPY app app

# install package from source
RUN chown -R floods: $FLOODS_HOME

# login as unpriviledged user as per Docker Best Practices
USER floods


# Development stage
FROM builder as dev
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0 


# Testing stage
FROM builder as test
ENV TESTING=1
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]


# Production stage
FROM builder as prod
CMD gunicorn wsgi:app \
      --log-level=${LOG_LEVEL} \
      --bind=${FLOODS_HOST}:${FLOODS_PORT} \
      --workers=2 \
      --threads=4 \
      --name floods

