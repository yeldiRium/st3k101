#!/usr/bin/env bash

echo "Starting dummy xAPI target..."

if [[ "$1" != "" ]]; then
    HOST="$1"
else
    HOST="127.0.0.1"
fi

export FLASK_APP=server.py
export FLASK_ENV=development
python -m flask run  --host=
