FROM jrc/smdrm_base as base
# SMDRM_HOME=/opt/smdrm

# set the working directory
WORKDIR $SMDRM_HOME/extract_tweets
COPY VERSION.txt .
COPY setup.py .
COPY src src

# become root to install the package
USER root

# install package from source
RUN pip install .

# login as unpriviledged user as per Docker Best Practices
USER smdrm

# task entrypoint
ENTRYPOINT ["extract_tweets"]
CMD ["--help"]


# Testing stage
FROM base as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]
