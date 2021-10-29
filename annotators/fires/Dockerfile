FROM python:3.8-slim-bullseye as dev

RUN python3 -m venv /app \
    && /app/bin/python -m pip install --no-cache-dir -U pip setuptools wheel

WORKDIR /app

COPY requirements.txt .
RUN bin/pip --no-cache-dir install -r requirements.txt

COPY README.md .
COPY api.py .
COPY src ./src
COPY tests ./tests

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    # print to stdout without buffering
    PYTHONDONTWRITEBYTECODE=1 \
    # don't generate *.pyc files
    PATH="/app/bin:$PATH"
    # export the python executable

CMD ["python", "api.py"]
