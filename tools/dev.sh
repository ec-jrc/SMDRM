#!/usr/bin/env bash

set -ue

HOST=$(hostname -i)
PORT=${PORT:-8888}

# start jupyter notebook
jupyter-notebook --no-browser --ip=$HOST --port=$PORT

