# syntax=docker/dockerfile:1
FROM libdrm

# set working directory
WORKDIR /home/smdrm/cache_tweets

# install elasticsearch client
RUN pip install elasticsearch==8.0.0

# copy source code
COPY --chown=1000:1000 VERSION.txt config.py cache_tweets.py ./
COPY --chown=1000:1000 tests tests

# runtime execution
CMD python cache_tweets.py --help

