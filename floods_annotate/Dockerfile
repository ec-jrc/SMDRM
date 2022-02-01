FROM smdrm/libdrm as builder

# SMDRM_HOME=/opt/smdrm
WORKDIR $SMDRM_HOME/floods_annotate

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy source code
COPY VERSION.txt .
COPY floods_annotate.py .


# Development stage
FROM builder as dev
CMD ["/bin/bash"]


# Testing stage
FROM builder as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]


# Staging stage
FROM builder as stg
CMD ["python", "floods_annotate.py", "--help"]

