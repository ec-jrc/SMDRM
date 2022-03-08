#!/usr/bin/env bash

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# user input path
INPUT_PATH=$1

if [ ! -f $INPUT_PATH ]; then
    echo not a file
    exit 1
fi

# copy given zipfile
cp $INPUT_PATH $CWD/data/imports/

# build image
docker-compose build trigger-dag-run

# run
docker-compose run --rm -e DEBUG=${DEBUG:-0} trigger-dag-run

