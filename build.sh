#!/bin/bash

if [ -z ${DOCKER_REGISTRY} ]; then
	echo "Environment Variable DOCKER_REGISTRY must be set."
	exit 1
fi

docker_registry=${DOCKER_REGISTRY}

info_message () {
	echo    "Usage:"
	echo -e "\tbuild command"
	echo    ""
	echo    "Commands:"
	echo -e "\tbuild   Build all images in this repository."
}

build () {
	find . -name Dockerfile -exec ./docker-build.sh {} $docker_registry \;
}

test () {
	find . -name Dockerfile -exec ./docker-test.sh {} \;
}

publish () {
	find . -name Dockerfile -exec ./docker-publish.sh {} $docker_registry \;
}


case $1 in
	build) build ;;
	test) test ;;
	publish) publish ;;
	run) build && test && publish ;;
	*) info_message ;;
esac