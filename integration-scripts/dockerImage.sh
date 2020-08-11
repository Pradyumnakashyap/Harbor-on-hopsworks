#!/usr/bin/env bash

set -e

help() {
    echo ""
    echo "usage: $0 [create docker_file tag] | [list image]"
    echo ""
    exit 1
}

TIMESTAMP=`date "+%Y%m%d%H%M%S"`
HARBOR_TAG="10.0.2.15:30003/harbor_test/conda_image:$TIMESTAMP"

VALID_IMAGE_NAME='^([a-z0-9]+(-[a-z0-9]+)*.)*[a-z0-9]+(:[0-9]*)?/[-:._a-zA-Z0-9]{0,62}[-:.a-zA-Z0-9]$'
if [ "$1" == "create" ] ; then

    # Sanity checks for injection attacks
    if [ ! -f "$2" ] ; then
	echo "Invalid docker file: $2" >&2
	help
    fi
    if ! [[ $3 =~ $VALID_IMAGE_NAME ]] ; then
	echo "error: Not an image name $3" >&2
	help
    fi
    
    DOCKER_BUILDKIT=1 docker build -f $2 --tag $3 ./

    docker tag $3 $HARBOR_TAG
    docker push $3
    docker push $HARBOR_TAG
    docker rmi $HARBOR_TAG	

elif [ "$1" == "delete" ] ; then
    # Sanity checks for injection attacks
    if ! [[ $2 =~ $VALID_IMAGE_NAME ]] ; then
	echo "error: Not an image name $3" >&2
	help
    fi

    if [[ "$(docker images -q $2 2> /dev/null)" == "" ]]; then
	exit 0
    else
	docker rmi -f $2
    fi
    
elif [ "$1" == "list" ] ; then
    if ! [[ $2 =~ $VALID_IMAGE_NAME ]] ; then
	echo "error: Not an image name $2" >&2
	help
    fi
    
    docker run --rm $2 conda list -n theenv

elif [ "$1" == "export" ] ; then
    if ! [[ $2 =~ $VALID_IMAGE_NAME ]] ; then
	echo "error: Not an image name $2" >&2
	help
    fi
    
    docker run --rm $2 conda env export -n theenv
    
else
    help
fi

exit $?
