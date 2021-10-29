FROM python:3.8-slim-bullseye
LABEL Author.Name="Emanuele Panizio" Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN python3 -m venv /upload \
    && /upload/bin/python -m pip install --no-cache-dir -U pip setuptools

WORKDIR /upload
COPY requirements.txt .
RUN bin/pip install --no-cache-dir -r requirements.txt

COPY ./api.py ./api.py
COPY ./README.md ./README.md

VOLUME /upload/uploads

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/upload/bin:$PATH"

CMD ["python", "api.py"]
