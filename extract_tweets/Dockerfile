FROM jrc/smdrm_base as base
# SMDRM_HOME=/opt/smdrm

# install packages
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy source code
COPY VERSION.txt .
COPY extract_tweets.py .
# task entrypoint
CMD ["python", "extract_tweets.py", "--help"]


# Testing stage
FROM base as test
RUN pip install pytest
COPY tests tests
ENTRYPOINT ["pytest"]
CMD ["--help"]
