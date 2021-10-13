#!/usr/bin/env bash

set -ue

local_dir=$1
clean=${2:-'n'}

# install dependencies
apt update && apt install git -y
python -m pip install laserembeddings


if [ "${clean}" == "y" ]; then
  # if clean, remove existing repo
  rm -r "${local_dir}"
fi

# make dir if cleaned or does not exist
mkdir -p "${local_dir}" && cd "${local_dir}"


if [ ! -f "${local_dir}/.git" ]; then
  # initialize repo if does not exist
  git init
  git remote add origin "https://smdrm_operational:QLQd74k98kW@bitbucket.org/lorinivalerio/smfr_models_data.git"
  git config core.sparseCheckout true
  # add the path to clone to the sparse-checkout file
  echo "models/*" >> .git/info/sparse-checkout
fi

# get last commit form origin master
git pull --depth=1 origin master

# download embeddings
if [ ! -d "${local_dir}/embeddings/" ]; then
  mkdir -p "${local_dir}/embeddings" && python -m laserembeddings download-models "${local_dir}/embeddings"
fi
