#!/bin/bash

dockerfile=$1
registry=$2
folder=$(dirname $dockerfile)
service=$(basename $folder)

name="$registry/uc/efla-$service:latest"

docker push $name