#!/usr/bin/env bash

set -ue

# current directory from any $pwd
CWD="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# build
bash $CWD/libdrm/build.sh dev
# run
docker run -it --rm \
  -e JUPYTER_TOKEN=docker \
  --network host \
  --volume $CWD:/opt/smdrm/ws \
  --workdir /opt/smdrm/ws \
  jrc/smdrm_dev
