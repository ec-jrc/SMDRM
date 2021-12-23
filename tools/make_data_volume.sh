#!/usr/bin/env bash

set -ue

# path to dir with zip files
DATA_DIR=${1}
echo "created $(docker volume create etl_data) volume"

echo "coping data from ${DATA_DIR} to volume"
docker run --rm \
  -v etl_data:/output \
  -v "${DATA_DIR}:/tmp/data" \
  alpine \
  cp -a /tmp/data/. /output
echo "copied"
