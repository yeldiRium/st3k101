#!/bin/bash

info_message () {
	echo    "Usage:"
	echo -e "\tbuild command [registry]"
	echo    ""
	echo    "Commands:"
	echo -e "\tbuild     Build images."
	echo -e "\ttest      Test images."
	echo -e "\tpublish   Publish images to registry."
	echo -e "\trun       Build, test and publish."
	echo    ""
	echo -e "Parameters: "
	echo -e "\tregistry  Docker registry in the form hostname[:port]."
	echo -e "\t          Required by build, publish and run."
}

check_registry () {
	if [ -z $docker_registry ]; then
		echo "Parameter registry is missing!"
		echo ""
		info_message
		exit 1
		fi
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

docker_registry=$2

case $1 in
	build) build ;;
	test) test ;;
	publish)
		check_registry
		publish
	;;
	run)
		check_registry
		build && test && publish
	;;
	*) info_message ;;
esac