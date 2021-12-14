FROM python:3.8-slim as base
# to serve as base image for extract and transform tweet services

LABEL Author.Name="Emanuele Panizio" \
      Author.Email="Emanuele.PANIZIO@ext.ec.europa.eu"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SMDRM_HOME=/opt/smdrm \
    PATH=$PATH:/opt/smdrm/.local/bin

# upgrade pip, setuptools, and wheel
# this enables the installation of pre-compiled packages
# create unpriviledged user
RUN pip install --upgrade pip setuptools wheel \
    && useradd -ms /bin/bash -d ${SMDRM_HOME} smdrm \
    && mkdir -p $SMDRM_HOME/libdrm

# set the working directory
WORKDIR $SMDRM_HOME

# copy source code
COPY VERSION.txt ./libdrm
COPY setup.py ./libdrm
COPY src ./libdrm/src

# install package from source
RUN pip install ./libdrm \
    && chown -R smdrm: $SMDRM_HOME

# login as unpriviledged user as per Docker Best Practices
USER smdrm


# Development stage
FROM base as dev
RUN pip install jupyter
ENV JUPYTER_TOKEN='changeme' \
    DEVELOPMENT=1
EXPOSE 8888
CMD jupyter-notebook --no-browser --ip=0.0.0.0 --port=8888


# Testing stage
FROM base as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]
