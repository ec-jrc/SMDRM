FROM python:3.8-alpine
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN python -m pip install --upgrade pip libdrm
WORKDIR /app

COPY test_annotate.py .
COPY cid_1210_dp_5000.zip .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "test_annotate.py"]
CMD ["--help"]
