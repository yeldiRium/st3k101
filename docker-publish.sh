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
	name="$dockeruser/efla-$service"
else
	name="$registry/$dockeruser/efla-$service"
fi

latest="$name:latest"
version="$name:$version"
sha="$name:$sha"

docker push "$latest"
docker push "$version"
docker push "$sha"
