#!/bin/bash -e

# This file should be run from src directory
# or as a first parameter you should specify
# path to the src

src=${1:-"."}

# grpc

protos_dir=$src/"protos"

for filepath in `ls $protos_dir/*.proto` ; do
    echo "Generating grpc files for ${mods[@]}"
    python -m grpc_tools.protoc -I$protos_dir --python_out=$src --grpc_python_out=$src $filepath
done

echo "Done!"
