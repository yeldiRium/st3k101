#!/bin/bash

set -e

dockerfile=$1
folder=$(dirname $dockerfile)
service=$(basename $folder)
sha=$(git rev-parse HEAD)

name="yeldir/efla-$service"

if [ -f "$folder/test.sh" ]; then
	sh -c "$folder/test.sh $name:$sha"
fi