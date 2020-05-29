                            Deploying a Ceph cluster on Kubernetes with a Rook Operator
                            
       
       
       1) Update Kubernetes cluster to v1.13+
       
       Follow the below link for updation without downtime. (Update Docker with the help of Docker_upgrade.txt)
            https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/
       
       2) Clone the GitHub Repository
       
          $ git clone https://github.com/rook/rook.git
          $ cd rook
          $ git checkout release-1.0 (All yaml files are configured based on this version)
          
       3) 
