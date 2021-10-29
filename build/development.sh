#!/usr/bin/env bash

# a standard development environment to develop, and test applications

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# run development service
docker run --rm -it \
  --gpus all \
  --name smdrm-dev \
  --network host \
  -v "${CWD}/..:/workspace" \
  -w /workspace \
  smdrm-dev:latest \
  bash "$@"
