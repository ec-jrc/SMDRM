FROM python:3.8-slim-bullseye as dev

RUN python3 -m venv /smdrm \
    && /smdrm/bin/python -m pip install --no-cache-dir -U pip setuptools wheel

WORKDIR /smdrm
COPY requirements.txt .
COPY ./libdrm/LICENSE.txt ./libdrm/LICENSE.txt
COPY ./libdrm/README.md ./libdrm/README.md
COPY ./libdrm/pyproject.toml ./libdrm/pyproject.toml
COPY ./libdrm/setup.cfg ./libdrm/setup.cfg
COPY ./libdrm/setup.py ./libdrm/setup.py
COPY ./libdrm/requirements.txt ./libdrm/requirements.txt
COPY ./libdrm/tests ./libdrm/tests
COPY ./libdrm/src ./libdrm/src

RUN bin/pip install --no-cache-dir -r requirements.txt libdrm/

ENV PYTHONUNBUFFERED=1 \
    # print to stdout without buffering
    PYTHONDONTWRITEBYTECODE=1 \
    # don't generate *.pyc files
    PATH="/smdrm/bin:$PATH"
    # export the python executable

CMD ["python"]
