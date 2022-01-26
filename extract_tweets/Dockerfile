FROM smdrm/libdrm as builder

# SMDRM_HOME=/opt/smdrm
WORKDIR $SMDRM_HOME/extract_tweets

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy source code
COPY VERSION.txt .
COPY extract_tweets.py .


# Development stage
FROM builder as dev
CMD ["python", "extract_tweets.py", "--help"]


# Testing stage
FROM builder as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]

