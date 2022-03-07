# syntax=docker/dockerfile:1
ARG DOCKER_HUB="index.docker.io"
FROM ${DOCKER_HUB}/python:3.8-slim

LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy \
    https_proxy=$https_proxy \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# create non priviledged user
RUN useradd -m smdrm
USER 1000

# prepare environment
ENV PATH=/home/smdrm/venv/bin:$PATH
WORKDIR /home/smdrm
RUN python -m venv venv; \
    pip install -U pip setuptools wheel

# copy source code
COPY --chown=1000:1000 setup.py libdrm/
COPY --chown=1000:1000 libdrm libdrm/libdrm
COPY --chown=1000:1000 tests libdrm/tests

# install libdrm
RUN pip install ./libdrm

# install task dependencies
# avoid reinstalling these deps for all tasks
RUN pip install pandas==1.4.1 requests==2.27.1

# runtime exec
CMD ["python"]
