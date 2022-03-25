# syntax=docker/dockerfile:1
FROM libdrm

# prepare environment
RUN mkdir -p api/instance/uploads api/instance/logs
WORKDIR /home/smdrm/api

# install dependencies
COPY --chown=smdrm:smdrm requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY --chown=smdrm:smdrm tests tests
COPY --chown=smdrm:smdrm apis apis
COPY --chown=smdrm:smdrm core core
COPY --chown=smdrm:smdrm apiv1.py .
COPY --chown=smdrm:smdrm run.py .

# exec
CMD python run.py
