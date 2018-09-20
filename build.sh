#!/bin/bash

docker_user=$2
docker_registry=$3

info_message () {
	echo    "Usage:"
	echo -e "\tbuild command name [registry]"
	echo    ""
	echo    "Commands:"
	echo -e "\tbuild     Build images."
	echo -e "\ttest      Test images."
	echo -e "\tpublish   Publish images to registry."
	echo -e "\trun       Build, test and publish."
	echo    ""
	echo -e "Parameters: "
	echo -e "\tregistry  Docker registry in the form hostname[:port]."
	echo -e "\t          If none is specified, docker hub is used."
	echo -e "\tname      Docker account name. Used to name images."
	echo    ""
	echo    "You need to manually log in to your docker registry"
	echo    "before running this script."
}

build () {
	find . -name Dockerfile -exec ./docker-build.sh {} $docker_user $docker_registry \;
}

test () {
	find . -name Dockerfile -exec ./docker-test.sh {} \;
}

publish () {
	find . -name Dockerfile -exec ./docker-publish.sh {} $docker_user $docker_registry \;
}

case $1 in
	build) build ;;
	test) test ;;
	publish)
		publish
	;;
	run)
		build && test && publish
	;;
	*) info_message ;;
esac