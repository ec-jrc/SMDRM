FROM jrc/smdrm_base as base
# SMDRM_HOME=/opt/smdrm

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy source code
COPY VERSION.txt .
COPY floods_annotate.py .
# task entrypoint
CMD ["python", "floods_annotate.py", "--help"]


# Testing stage
FROM base as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]
