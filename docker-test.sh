#!/bin/bash

dockerfile=$1
folder=$(dirname $dockerfile)
service=$(basename $folder)
sha=$(git rev-parse HEAD)

name="yeldir/efla-$service"

sh -c "$folder/docker-test.sh $name:$sha"