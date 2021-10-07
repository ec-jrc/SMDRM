#!/usr/bin/env bash

set -ue

# define project root directory from current
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "Upload a file.zip to an observed directory."
echo "Notes: other extensions won't be considered."

read -r -p "path: " file_to_upload

cp "${file_to_upload}" "${CWD}/engine/uploads"
