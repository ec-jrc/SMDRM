FROM python:3.8-slim-bullseye as dev

RUN python3 -m venv /smdrm \
    && /smdrm/bin/python -m pip install --no-cache-dir -U pip setuptools

WORKDIR /smdrm
COPY requirements.txt .
RUN bin/pip install --no-cache-dir -r requirements.txt

ENV LOG_LEVEL=DEBUG \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/smdrm/bin:$PATH"

CMD ["python"]
