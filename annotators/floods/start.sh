#!/usr/bin/env bash

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# make model dir if does not exist
MODEL_DIR=${1:-"${CWD}/models"}
mkdir -p $MODEL_DIR

# download models
if [ ! -f "$MODEL_DIR/lasermultilingual.model.h5" ]; then
  echo model not found, downloading from Zenodo...
  cd $MODEL_DIR
  curl -o model.zip "https://zenodo.org/record/6351658/files/ec-jrc-floods-annotator.zip?download=1"
  unzip model.zip && rm model.zip
  cd -
fi

# download embeddings
if [ ! -f "$MODEL_DIR/bilstm.93langs.2018-12-26.pt" ]; then
  echo embeddings not found, downloading Laserembeddings binary models...
  python -m laserembeddings download-models $MODEL_DIR 
fi

# start app
flask run --host=0.0.0.0 --port=5000

