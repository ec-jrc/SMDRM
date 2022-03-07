#!/usr/bin/env bash

set -ue

echo download model components
python -m deeppavlov download $CONFIG

echo start REST API
python api.py

