FROM libdrm

# set env variables
ENV FILENAME= \
    DEBUG=0

# enable REST API framework
RUN pip install requests

# set workdir
# HOME=/opt/smdrm
# PWD=$HOME/libdrm
WORKDIR /opt/smdrm/data

# create export DB volume
VOLUME ./airflow

# copy into image
COPY --chown=smdrm:smdrm trigger_dag_run.py .

# execute at runtime
CMD ["python", "trigger_dag_run.py"]

