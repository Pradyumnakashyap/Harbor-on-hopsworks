# Persistent Volumes and Persistent Volume Claims with Kubernetes Node's local-disk Storage

### Host filesystem storage with local storage class, persistent volumes and persistent volume claims

![Node Storage with Kubernetes](PV.jpg)


The Kubernetes node consists of a host filesystem as part of its operating system.
We create storage classes on these host filesystems by providing paths on the node
and deploying persistent volumes for these storage classes.
Further the applications use persistent volume claims to use the persistent volumes 
and store the application data on the host filesystem as persistent storage. This 
helps to persist the data upon Kubernetes pods lifecycle. 

 
 
