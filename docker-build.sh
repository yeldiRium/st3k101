#!/bin/bash

dockerfile=$1
registry=$2
folder=$(dirname $dockerfile)
service=$(basename $folder)
version=$(cat "$folder/Version")
sha=$(git rev-parse HEAD)

name="$registry/uc/efla-$service"

docker build $folder -t "$name:latest" -t "$name:$version" -t "$name:$sha"