#!/usr/bin/env bash

set -xe

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# build docker image
DOCKER_BUILDKIT=1 docker build -t dev/smdrm:latest "${CWD}/"