#!/usr/bin/env bash

set -e

# run SMDRM Docker base image tests
docker run --rm "jrc/floods_annotate_test" .
