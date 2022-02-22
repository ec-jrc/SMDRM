FROM libdrm as builder

# SMDRM_HOME=/opt/smdrm
WORKDIR $SMDRM_HOME/geocode_tweets

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy source code
COPY VERSION.txt .
COPY config config
COPY geocode_tweets.py .


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
CMD ["python", "geocode_tweets.py", "--help"]

