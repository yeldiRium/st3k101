#!/bin/bash

image=$1

# cd to frontend dir
cd "$(dirname "$0")"

npm install

node ./node_modules/.bin/greenkeeper-lockfile-update

echo "No tests configured for frontend."

node ./node_modules/.bin/greenkeeper-lockfile-upload

# cd back
cd -
