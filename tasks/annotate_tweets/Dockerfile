# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/annotate_tweets

# copy source code
COPY VERSION.txt .
COPY annotate_tweets.py .
COPY tests tests

# runtime execution
CMD python annotate_tweets.py --help

