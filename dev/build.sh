#!/usr/bin/env bash

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# build docker image
docker build -t "dev/smdrm:v1" "${CWD}/"
