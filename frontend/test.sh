#!/bin/bash -e

image=$1

# cd to frontend dir
cd "$(dirname "$0")"

npm install

node ./node_modules/.bin/greenkeeper-lockfile-update

npm run test

node ./node_modules/.bin/greenkeeper-lockfile-upload

# cd back
cd -
