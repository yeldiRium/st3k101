#!/bin/bash

set -e

dockerfile=$1
dockeruser=$2
registry=$3
folder=$(dirname $dockerfile)
service=$(basename $folder)
version=$(cat "$folder/Version")
sha=$(git rev-parse HEAD)

if [ -z $registry ]; then
	name="$dockeruser/st3k101-$service"
else
	name="$registry/$dockeruser/st3k101-$service"
fi

docker build $folder -t "$name:latest" -t "$name:$version" -t "$name:$sha"