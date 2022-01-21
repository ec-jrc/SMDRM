#!/usr/bin/env bash

set -ue

# build SMDRM Task

# set project root directory
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# global environment variables
export $(grep -v '^#' "${ROOT}/.env" | xargs)

# task ID to build
TASK=${1}
# task directory
TASK_DIR="${ROOT}/${TASK}"

# docker tag
IMAGE="smdrm/${TASK}"
VERSION=`cat $TASK_DIR/VERSION.txt`
TAG="${IMAGE}:${VERSION}-${ENV}"

# build
echo "Building ${TAG}"
docker build -t $TAG \
  --build-arg DOCKER_HUB=${DOCKER_HUB:="index.docker.io"} \
  --build-arg http_proxy=${http_proxy:=""} \
  --build-arg https_proxy=${https_proxy:=""} \
  --target $ENV \
  "$TASK_DIR/"
# add latest tag
docker tag $TAG "${IMAGE}:latest"

