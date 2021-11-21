FROM python:3.8-slim-bullseye as base
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN python3 -m venv /app \
    && /app/bin/python -m pip install --no-cache-dir -U pip setuptools

WORKDIR /app
COPY requirements.txt .
RUN bin/pip install --no-cache-dir -r requirements.txt

COPY api.py .
COPY annotator.py .
COPY README.md .

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/bin:$PATH"

ENTRYPOINT ["bin/python", "api.py"]
CMD ["--help"]


FROM base as test
WORKDIR /app
COPY --from=base /app .
RUN python -m pip install pytest requests

COPY tests ./tests
ENTRYPOINT ["bin/pytest"]
CMD ["tests/unit"]
