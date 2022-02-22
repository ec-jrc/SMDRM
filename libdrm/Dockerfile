ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.8-slim as builder

# to serve as base image for extract and transform tweet services
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ARG SMDRM_HOME=/opt/smdrm
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy https_proxy=$https_proxy

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=$PATH:${SMDRM_HOME}/.local/bin

# upgrade pip, setuptools, and wheel
# this enables the installation of pre-compiled packages
# create unpriviledged user
RUN pip install --upgrade pip setuptools wheel \
    && useradd -ms /bin/bash -d ${SMDRM_HOME} smdrm

# set the working directory
WORKDIR ${SMDRM_HOME}/libdrm

# copy source code
COPY VERSION.txt .
COPY setup.py .
COPY src src

# install package from source
RUN pip install . \
    && chown -R smdrm:0 ${SMDRM_HOME}

# login as unpriviledged user as per Docker Best Practices
USER smdrm


# Development stage
FROM builder as dev
RUN pip install jupyter
CMD ["python"]


# Testing stage
FROM builder as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]

