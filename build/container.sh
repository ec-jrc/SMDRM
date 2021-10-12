#!/usr/bin/env bash

set -ue

## check if process is running inside a docker container
#if [ -f "/.dockerenv" ]; then
#  # activate env and get ready for user commands if true
#  echo "in docker"
#  source . /opt/venv/bin/activate
#  exec "$@"
#else
#  # run the container and access above condition if false
#  echo "running container"
#  docker run --rm -it\
#    --name smdrm-dev \
#    -w /workspace \
#    -v "${PWD}/../tools:/workspace/tools" \
#    -v "${PWD}/../libdrm:/workspace/libdrm" \
#    smdrm/workspace:v1.0 \
#    bash "$@"
#fi

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# run in development mode
docker run --rm -it \
  --name smdrm-dev \
  --network smdrm_backend \
  -v "${CWD}/..:/workspace" \
  -w /workspace \
  dev/smdrm:latest \
  bash "$@"
