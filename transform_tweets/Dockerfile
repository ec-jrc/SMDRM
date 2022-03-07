# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/transform_tweets

# copy source code
COPY VERSION.txt .
COPY transformations.py .
COPY transform_tweets.py .
COPY tests tests

# runtime execution
CMD python transform_tweets.py --help

