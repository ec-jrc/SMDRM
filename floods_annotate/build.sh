#!/usr/bin/env bash

set -ue

# build SMDRM Extract Tweets ETL step
CWD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# environment
ENV="${1:-$ENV}"

# docker tag
IMAGE="jrc/floods_annotate"
VERSION=`cat $CWD/VERSION.txt`
TAG="${IMAGE}_${ENV}:${VERSION}"

# build
echo "Building ${TAG}"
docker build -t $TAG --target $ENV "$CWD/"

# add latest tag
docker tag $TAG "${IMAGE}_${ENV}:latest"
