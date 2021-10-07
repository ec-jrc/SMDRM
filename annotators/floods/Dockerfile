FROM python:3.8-slim as builder
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYENV=/floods/venv \
    ROOT_DIR=/floods

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
# copy resources into image
COPY ./VERSION.txt ./VERSION.txt
COPY ./README.md ./README.md
COPY ./tests ./tests
COPY ./src ./src
COPY ./api.py ./api.py

# start api
CMD python api.py


FROM python:3.8-alpine3.14 as production
LABEL author="emanuele.panizio@ext.ec.europa.eu"

# prepare workspace
WORKDIR $ROOT_DIR
COPY --from=builder $ROOT_DIR ./
ENV USER=drm GROUP=docker PATH="$PYENV/bin:$PATH"
RUN set -ex;\
    # create a group and user
    addgroup -S $GROUP && adduser -S $USER -G $GROUP; \
    # assign permissions
    chown -R $USER:$GROUP $ROOT_DIR
# set new user
USER $USER

# start api
ENTRYPOINT python api.py
