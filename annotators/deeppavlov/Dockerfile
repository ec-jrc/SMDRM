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
    PORT=5000 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    DEEPPAVLOV_HOME=/opt/deeppavlov

RUN apt update \
    && apt install -y \
      gcc \
      g++ \
      git; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --upgrade pip setuptools wheel; \
    useradd -ms /bin/bash -d $DEEPPAVLOV_HOME deeppavlov

# set the working directory
WORKDIR $DEEPPAVLOV_HOME

# deeppavlov uses the user home to install
# models and config into .deeppavlov/
VOLUME $DEEPPAVLOV_HOME/.deeppavlov

# copy source code, and download instructions
COPY download.py .
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && python -m deeppavlov install squad_bert \
    && python download.py
COPY api.py .

# install package from source
RUN chown -R deeppavlov: $DEEPPAVLOV_HOME

# login as unpriviledged user as per Docker Best Practices
USER deeppavlov

CMD python api.py --host=$HOST --port=$PORT
