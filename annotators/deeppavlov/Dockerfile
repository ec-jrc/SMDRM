FROM python:3.7-slim
LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ENV CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST="0.0.0.0" \
    PORT=4000 \
    TF_CPP_MIN_LOG_LEVEL=2

RUN apt update \
    && apt install -y \
      gcc \
      g++ \
      git; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --upgrade pip

WORKDIR /deeppavlov

COPY requirements.txt .
COPY download.py .
COPY ner_ontonotes_bert_mult.json .
RUN pip install -r requirements.txt; \
    # trick to change DeepPavlov models locations
    cp ner_ontonotes_bert_mult.json /usr/local/lib/python3.7/site-packages/deeppavlov/configs/ner/ner_ontonotes_bert_mult.json; \
    python -m deeppavlov install squad_bert; \
    python download.py

COPY README.md .
COPY api.py .

CMD python api.py --host=$HOST --port=$PORT
