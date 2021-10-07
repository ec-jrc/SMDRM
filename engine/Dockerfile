FROM python:3.9-slim as builder
ENV DEBIAN_FRONTEND=noninteractive \
    PYENV=/engine/venv \
    ROOT_DIR=/engine

# prepare workspace
WORKDIR $ROOT_DIR
COPY ./requirements.txt ./requirements.txt
RUN set -ex; \
    # update OS
    apt update && apt clean && rm -rf /var/lib/apt/lists/*; \
    # make virtual env
    python3 -m venv $PYENV; \
    # install pip dependencies
    ./venv/bin/python3 -m pip install -U pip wheel -r requirements.txt
# update PATH with python env
ENV PATH="$PYENV/bin:$PATH"
# copy app source code to container
COPY ./tests ./tests
COPY ./apis.py ./apis.py
COPY ./start.py ./start.py
COPY ./README.md ./README.md
COPY ./VERSION.txt ./VERSION.txt

# uploads volume
VOLUME $ROOT_DIR/uploads $ROOT_DIR/logs

# start observer
CMD python start.py
