# syntax=docker/dockerfile:1
FROM libdrm

# prepare environment
RUN mkdir -p ui/instance/uploads
WORKDIR /home/smdrm/ui

# install dependencies
COPY --chown=smdrm:smdrm requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY --chown=smdrm:smdrm server server
COPY --chown=smdrm:smdrm client client
