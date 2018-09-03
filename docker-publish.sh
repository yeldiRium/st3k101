#!/bin/bash

dockerfile=$1
registry=$2
folder=$(dirname $dockerfile)
service=$(basename $folder)
version=$(cat "$folder/Version")
sha=$(git rev-parse HEAD)

name="$registry/uc/efla-$service"
latest="$name:latest"
version="$name:$version"
sha="$name:$sha"

docker push "$latest"
docker push "$version"
docker push "$sha"
