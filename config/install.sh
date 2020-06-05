#!/bin/bash

# Check Docker version

set -e
set -o noglob

if ! docker --version &> /dev/null
then
	echo "Docker environment not present!"
        exit 1 
fi


# Check for kubernetes cluster and store the master node ip for harbor installation


master_exists=$(kubectl cluster-info  | grep master | grep -o -P 'https://.{0,20}' | cut -c 9-)

[ -z "$master_exists" ] && echo "Kubernetes cluster is not running" && exit 1

masterip=$(kubectl get nodes -o wide | awk 'NR==2{print $6}')
masternode=$(kubectl get nodes -o wide | awk 'NR==2{print $1}')


# Create multiple YAML objects from stdin
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: registry-pv
spec:
  capacity:
    storage: 30Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: local-storage
  local:
    path: /mnt/disk/vol1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - $masternode
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: harbor-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 30Gi
EOF

# Helm charts to run Harbor

helm repo add harbor https://helm.goharbor.io
helm repo add stable https://kubernetes-charts.storage.googleapis.com

helm install harbor --debug harbor/harbor --set expose.type=nodePort --set expose.tls.commonName=$masterip --set externalURL=https://$masterip:30003 --set persistence.persistentVolumeClaim.registry.existingClaim='harbor-claim' --set persistence.persistentVolumeClaim.chartmuseum.existingClaim='harbor-claim' --set persistence.persistentVolumeClaim.jobservice.existingClaim='harbor-claim' --set persistence.persistentVolumeClaim.database.existingClaim='harbor-claim' --set persistence.persistentVolumeClaim.redis.existingClaim='harbor-claim' --set version='v1.10.1'


