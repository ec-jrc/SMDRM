#!/usr/bin/env bash

# this is a development environment
# it serves as standard workspace to develop, and test

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# run in development mode
docker run --rm -it \
  --name smdrm-dev \
  --network host \
  -v "${CWD}/..:/workspace" \
  -w /workspace \
  dev/smdrm:latest \
  bash "$@"
