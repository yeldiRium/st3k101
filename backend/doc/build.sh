#!/usr/bin/env bash

echo "Entering virtualenv ..."
source .sphinx-venv/bin/activate

# set up environment from environment files. The code won't work without.
echo "Setting envvars..."
envVarsSetByThisScript=()
while read line; do

    if [ -z $line ]; then
        continue
    fi

    keyValue=(${line//=/ })  # split at =
    envVar=${keyValue[0]}
    if [ -z ${!envVar+x} ]; then  # check if envvar is already set
        echo " -> set $envVar ..."
        export $line
        envVarsSetByThisScript+=( "$envVar" )
    else
        echo "    WARNING: ${envVar} is set to '${!envVar}', leaving it unchanged."
    fi

done < ../../backend.env;

# Set up environment variables from dockerfile
if [ -z ${FLASK_CONFIG_PATH+x} ]; then
    export FLASK_CONFIG_PATH=../app/flask.cfg
    envVarsSetByThisScript+=( "FLASK_CONFIG_PATH" )
else
    echo "WARNING: FLASK_CONFIG_PATH already set, leaving it unchanged."
fi

# clean build
make clean

# generate and build docs
echo "Running sphinx-apidoc ..."
sphinx-apidoc -f -o source ../app &>build.log
echo "Running sphinx-build ..."
sphinx-build -b html source build &>build.log

echo "Cleaning up envvars ..."
for key in "${envVarsSetByThisScript[@]}";
do
    echo "-> unset $key ..."
    unset $key
done

echo "Leaving virtualenv ..."
deactivate
