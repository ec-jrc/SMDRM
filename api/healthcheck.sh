#!/usr/bin/env bash

set -ue

CONTAINER_IP=$(hostname -I | awk '{print $1}')

curl --fail "http://${CONTAINER_IP}:5000/api/v1/info/health" || exit 1
