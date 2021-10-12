FROM dev/smdrm:latest as builder
ENV DEBIAN_FRONTEND=noninteractive \
    ROOT_DIR=/engine

# prepare workspace
WORKDIR $ROOT_DIR
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt
# copy app source code to container
COPY ./tests ./tests
COPY ./apis.py ./apis.py
COPY ./start.py ./start.py
COPY ./README.md ./README.md
COPY ./VERSION.txt ./VERSION.txt

# uploads volume
VOLUME /engine/uploads /engine/logs

# start engine
ENTRYPOINT ["python", "start.py"]
CMD []
