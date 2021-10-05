FROM python:3.9-slim as builder
ENV DEBIAN_FRONTEND=noninteractive \
    PYENV=/engine/venv \
    ROOT_DIR=/engine

# prepare workspace
WORKDIR $ROOT_DIR
COPY ./requirements.txt ./requirements.txt
RUN set -ex; \
    # update OS
    apt-get update; \
    # make virtual env
    python3 -m venv $PYENV; \
    # install pip dependencies
    ./venv/bin/pip install --upgrade pip -r requirements.txt
# update PATH with python env
ENV PATH="$PYENV/bin:$PATH"
# copy app source code to container
COPY ./src ./src
COPY ./start.py ./start.py
COPY ./README.md ./README.md
COPY ./VERSION.txt ./VERSION.txt

# uploads volume
VOLUME $ROOT_DIR/data

# start observer
CMD python start.py
