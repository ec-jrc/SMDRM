FROM python:3.8-slim-bullseye
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN python3 -m venv /app \
    && /app/bin/python -m pip install --no-cache-dir -U pip setuptools

WORKDIR /app
COPY requirements.txt .
RUN bin/pip install --no-cache-dir -r requirements.txt

COPY README.md .
COPY api.py .
COPY src ./src

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/bin:$PATH"

ENTRYPOINT ["bin/python", "api.py"]
CMD ["--help"]
