FROM jrc/smdrm_base
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

RUN pip install --upgrade pip requests

WORKDIR /perftests
COPY test_annotate.py .
COPY cid_1210_5k_ext.zip .

ENTRYPOINT ["python", "test_annotate.py"]
CMD ["--help"]
