#!/usr/bin/env bash

set -ue

# set the type of image to build
TARGET=${1:-"dev"}
# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# build docker image
DOCKER_BUILDKIT=1 docker build --target "${TARGET}" -t "smdrm-${TARGET}:latest" "${CWD}/"
