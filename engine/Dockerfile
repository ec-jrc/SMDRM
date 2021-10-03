FROM python:3.9-slim as builder
ARG NAME=observer
ENV DEBIAN_FRONTEND=noninteractive \
    PYENV=/${NAME}/venv \
    LOGROTATE_PATH=/var/log/smdrm/rotate

# prepare workspace
WORKDIR /${NAME}
COPY ./requirements.txt ./requirements.txt
RUN set -ex; \
    # update OS
    apt-get update; \
    # make virtual env
    python3 -m venv "${PYENV}"; \
    # install pip dependencies
    ./venv/bin/pip install --upgrade pip -r requirements.txt
# update PATH with python env
ENV PATH="$PYENV/bin:$PATH"
# copy app source code to container
COPY ./start.py ./start.py
COPY ./README.md ./README.md
COPY ./VERSION.txt ./VERSION.txt

# start observer
CMD python start.py --observed-path $LOGROTATE_PATH
