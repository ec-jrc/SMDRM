# syntax=docker/dockerfile:1
FROM libdrm

USER root
RUN apt update; \
    apt install -y curl
USER smdrm

# prepare environment
RUN mkdir -p api/instance/uploads api/instance/logs
WORKDIR /home/smdrm/api

# install dependencies
COPY --chown=smdrm:smdrm requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY --chown=smdrm:smdrm tests tests
COPY --chown=smdrm:smdrm api api
COPY --chown=smdrm:smdrm apiv1.py .
COPY --chown=smdrm:smdrm wsgi.py .

# healthcheck
COPY --chown=smdrm:smdrm healthcheck.sh .
RUN chmod +x ./healthcheck.sh
HEALTHCHECK --interval=60s --timeout=10s CMD /home/smdrm/api/healthcheck.sh

# exec
CMD python wsgi.py --host=$(hostname -I | awk '{print $1}')
