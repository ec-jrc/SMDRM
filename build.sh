#!/usr/bin/env bash

set -ue

# build SMDRM ETL images
ENV=${1:-base}

# base image with libdrm core module
bash $(pwd)/libdrm/build.sh $ENV

# tasks
bash $(pwd)/extract_tweets/build.sh $ENV
bash $(pwd)/transform_tweets/build.sh $ENV

# annotation plugins
#docker-compose up --build
