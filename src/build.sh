#!/bin/bash -e

# This file should be run from src directory
# or as a first parameter you should specify
# path to the src

src=${1:-"."}

# grpc

protos_dir=$src/"protos"

PYTHON3=$(which python3)

for filepath in `ls $protos_dir/*.proto` ; do
    file=$(basename $filepath)
    echo "Generating grpc files for ${file%.*}..."
    $PYTHON3 -m grpc_tools.protoc -I$protos_dir --python_out=$src --grpc_python_out=$src $filepath
done

echo "Done!"


# animal model weights

echo "Pulling large files from git..."

git lfs pull

echo "Done!"
