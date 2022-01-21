#!/usr/bin/env bash

set -ue

# current directory from any $pwd
CWD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# choose dev image version
VERSION=${1:-latest}

# run
docker container run -it --rm \
  -e JUPYTER_TOKEN=docker \
  --network host \
  --volume $CWD:/opt/smdrm/ws \
  --workdir /opt/smdrm/ws \
  smdrm/libdrm:${VERSION}

