#!/usr/bin/env bash

set -ue

HOST=$(hostname -i)
PORT=${PORT:-8888}

# install framework
pip install notebook

# start jupyter notebook
jupyter-notebook --no-browser --ip=$HOST --port=$PORT

