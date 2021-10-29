FROM python:3.8-slim-bullseye
LABEL Author.Name="Emanuele Panizio" Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN python3 -m venv /engine \
    && /engine/bin/python -m pip install --no-cache-dir -U pip setuptools

WORKDIR /engine
COPY requirements.txt .
RUN bin/pip install --no-cache-dir -r requirements.txt

COPY ./README.md ./README.md
COPY ./tests ./tests
COPY ./api.py ./api.py

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/engine/bin:$PATH"

CMD ["python", "api.py"]
