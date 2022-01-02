#!/usr/bin/env bash

set -ue

# laserembeddings is required
# pip install laserembeddings

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
local_dir=${1:-"${CWD}/models"}
echo "downloading models into $local_dir..."

# make dir if cleaned or does not exist
mkdir -p "${local_dir}" && cd "${local_dir}"

# initialize repo if does not exist
if [ ! -f "${local_dir}/.git" ]; then
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
  echo "download embeddings"
  mkdir -p "${local_dir}/embeddings" && python -m laserembeddings download-models "${local_dir}/embeddings"
fi
