# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/extract_tweets

# copy source code
COPY VERSION.txt .
COPY extract_tweets.py .
COPY tests tests

# runtime execution
CMD python extract_tweets.py --help

