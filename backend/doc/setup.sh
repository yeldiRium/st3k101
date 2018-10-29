#!/usr/bin/env bash
echo "Do NOT run this from a virtualenv!"
echo "It will install requirements to it, if you don't deactivate it first."
while true; do
    read -p "Start setup? (y/n) " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) echo "Kthxbye!"; exit;;
        * ) echo "Kthxbye!"; exit;;
    esac
done

echo "Creating virtualenv ..."
virtualenv .sphinx-venv --python=python3 &>setup.log

echo "Installing requirements ..."
source ./.sphinx-venv/bin/activate
pip install -r ../app/requirements.txt &>setup.log
pip install sphinx &>setup.log
deactivate

echo "All set up!"
echo "You may now run build.sh"
