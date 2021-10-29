FROM smdrm-dev:latest as dev
ENV DEBIAN_FRONTEND=noninteractive \
    ROOT_DIR=/engine

# prepare workspace
WORKDIR $ROOT_DIR
COPY ./requirements.txt ./requirements.txt
RUN python -m pip --no-cache-dir install -r requirements.txt
# copy app source code to container
COPY ./tests ./tests
COPY ./api.py ./api.py
COPY ./README.md ./README.md

# start engine
ENTRYPOINT ["python", "api.py"]
CMD []
