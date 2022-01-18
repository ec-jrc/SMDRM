FROM jrc/smdrm_base as base

# SMDRM_HOME=/opt/smdrm
WORKDIR $SMDRM_HOME/geocode_tweets

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY VERSION.txt .
COPY config config
COPY geocode_tweets.py .

# task entrypoint
CMD ["python", "geocode_tweets.py", "--help"]


# Testing stage
FROM base as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]
