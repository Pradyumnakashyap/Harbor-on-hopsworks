#!/bin/bash

# Install helm and move to the correct path - ***Root user privileges are required***

set +e

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
temp=$(./get_helm.sh)

mv /usr/local/bin/helm /usr/bin

if ! helm version &> /dev/null
then
	echo "Helm installation failed, Please try installing manually"
        exit 1
else

	rm -rf get_helm.sh

	# Create the folder for the local persistent volumes

	mkdir -p /mnt/disk/vol1

	echo "Installation and configuration complete!"
fi



