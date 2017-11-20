#!/usr/bin/env bash
read -p "Warning: This will remove all stopped containers and delete their storage. Continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker-compose down
    yes | docker container prune
    yes | docker volume prune
    docker-compose build --no-cache
fi
