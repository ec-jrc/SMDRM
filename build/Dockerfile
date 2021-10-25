FROM python:3.8-slim
# prepare workspace
COPY ./requirements.txt /requirements.txt
COPY ./libdrm /libdrm
RUN set -xe; \
    # update OS
    apt update && apt upgrade -y && apt clean && rm -rf /var/lib/apt/lists/*; \
    # make python virtual environment
    python3 -m venv /opt/venv; \
    # upgrade, install dependencies, and core libs
    /opt/venv/bin/python3 -m pip install -U pip wheel -r /requirements.txt /libdrm
# update PATH with python env
ENV PATH="/opt/venv/bin:$PATH"
# execute this
CMD ["python"]
