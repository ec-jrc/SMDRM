FROM python:3.9-slim as builder
ENV DEBIAN_FRONTEND=noninteractive \
    PYENV=/uploader/venv \
    ROOT_DIR=/uploader

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
COPY ./api.py ./api.py
COPY ./README.md ./README.md
COPY ./VERSION.txt ./VERSION.txt

# uploads volume
VOLUME "$ROOT_DIR/data"

# start uploader
CMD ["python", "api.py"]


FROM python:3.9-alpine3.14 as production
LABEL author="emanuele.panizio@ext.ec.europa.eu"

# prepare workspace
WORKDIR $ROOT_DIR
COPY --from=builder $ROOT_DIR ./
ENV USER=drm GROUP=docker \
    PATH="$PYENV/bin:$PATH" \
    LOG_PATH=/var/log/smdrm

# output directory for uploaded data
VOLUME "$ROOT_DIR/data"

RUN set -ex;\
    # create a group and user
    addgroup -S $GROUP && adduser -S $USER -G $GROUP; \
    # assign permissions
    chown -R $USER:$GROUP /$NAME $LOG_PATH
# set new user
USER $USER

# start uploader
ENTRYPOINT ["python", "api.py"]
CMD []
