#!/usr/bin/env bash

set -e

# run SMDRM Docker base image tests
docker run --rm "e1/smdrm_test:1.0" .
