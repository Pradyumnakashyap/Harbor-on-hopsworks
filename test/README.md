# Tests to determine push and pull performances of Harbor registry on different storage architectures


### Functionality 

The performance metrics python script does the following : 

Prerequisite : Deploy harbor registry from scratch. We should be sure that there is no data in the form of repositories or images in it.

1) Push Concurrency 

a. First the script builds 100 images based on the Dockerfile in the mentioned path.
b. It then runs a client in the cycle with ITERATIONS_COUNT iterations and CONCURRENCY concurrency value. 
   The client should be able to push the images which we created on the previous step and write a response time to a log/report. 
   Manually, we need to perform one cycle per each CONCURRENCY value from the following list:

- CONCURRENCY=1
- CONCURRENCY=3
- CONCURRENCY=6

c. As a result of the previous step we are able to provide graphs and tables with the dependences on an iteration number of a response time. 
One graph and one table per each CONCURRENCY.

2) Pull Concurrency

a. First the script builds 100 images based on the Dockerfile in the mentioned path.
b. Next, it uploads 100 images to the repository
c. Further deletes created images from a local docker on a machine with test tool where docker images was created. 
After this step created images should be placed in the repository and they should be removed from the local docker.
d. It then runs a client in the cycle with ITERATIONS_COUNT iterations and CONCURRENCY concurrency value. 
  The client should be able to pull the images which we uploaded on the previous step and write a response time to a log/report. 
  Manually, we need to perform one cycle per each CONCURRENCY value from the following list:

- CONCURRENCY=1
- CONCURRENCY=3
- CONCURRENCY=6

e. As a result of the previous step we are able to provide graphs and tables with the dependences on an iteration number of a response time. 
One graph and one table per each CONCURRENCY.

Following custom values can be changed in the script :

- iterations: number of images which should be created, uploaded to a repository and downloaded from the repository.
- concurrency: number of threads which should work at the same time.
- repo_address address and port of a repository service.

### Testing Process: 

1. Harbor Registry was installed on top of a server with host Ip = 172.20.9.16:30003
2. The values of the variables in perf-metrics.py script to be changed: iterations = 1000 concurrency = 1 repo_address = “172.20.9.16:30003”
3. The following command was executed to perform the tests: 
    
    $ sudo docker login -u $username -p $password 172.20.9.16:30003
    $ sudo python perf-metrics.py
 
4. push_results.csv and pull_results.csv saved in a persistent folder for analysis.
5. The steps from 1 through to 4 are repeated with change in concurrency parameter values 
   values: 1,3,6
   
