FROM python:3.9-slim as dev

# default env
ENV RABBITMQ_QUEUE="sanitize" \
    RABBITMQ_HOST="rabbitmq"

# change to app directory
WORKDIR /file_uploader

# prepare environemt
COPY ./requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip; \
    pip3 install -r ./requirements.txt

# copy app source code to container
COPY ./README.md ./README.md
COPY ./start.py ./start.py
COPY ./src ./src
COPY ./tests ./tests

# run gunicorn server and wait on incoming requests
ENTRYPOINT ["python3", "start.py", "--path", "/tmp/observed"]
CMD []
