#!/usr/bin/env bash

# this is a development environment
# it serves as standard workspace to develop, and test

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# create smdrm backend network if it does not exist
# it enables containers communications
docker network create smdrm_backend || true

# run in development mode
docker run --rm -it \
  --name smdrm-dev \
  --network smdrm_backend \
  -v "${CWD}/..:/workspace" \
  -w /workspace \
  dev/smdrm:latest \
  bash "$@"
