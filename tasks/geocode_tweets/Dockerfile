# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/geocode_tweets

# copy source code
COPY VERSION.txt .
COPY config config
COPY tests tests
COPY geocode_tweets.py .

# runtime execution
CMD python geocode_tweets.py --help

