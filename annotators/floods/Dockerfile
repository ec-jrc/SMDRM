FROM python:3.8-slim as builder
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    ROOT_DIR=/floods

# prepare workspace
WORKDIR $ROOT_DIR
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install -U pip -r requirements.txt
# copy resources into image
COPY ./README.md ./README.md
COPY ./tests ./tests
COPY ./src ./src
COPY ./api.py ./api.py

# start api
ENTRYPOINT ["python3", "api.py"]
CMD []


FROM python:3.8-alpine3.14 as production
LABEL author="emanuele.panizio@ext.ec.europa.eu"

# prepare workspace
WORKDIR $ROOT_DIR
COPY --from=builder $ROOT_DIR ./
ENV USER=drm GROUP=docker
RUN set -xe;\
    # create a group and user
    addgroup -S $GROUP && adduser -S $USER -G $GROUP; \
    # assign permissions
    chown -R $USER:$GROUP $ROOT_DIR
# set new user
USER $USER

# start api
ENTRYPOINT ["python", "api.py"]
CMD []
