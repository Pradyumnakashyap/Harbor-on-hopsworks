#!/usr/bin/python

try:
    import docker
    import request
    import sys
    import time
    import subprocess
    import requests
    import json

except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import requests
    import sys
    import time
    import subprocess
    import requests
    import json

def run_command(command):
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise Exception('Error: Exited with error code: {}. Output:{}'.format(e.returncode, e.output))

def docker_login(harbor_host, user, password):
        command = ["sudo", "docker", "login", harbor_host, "-u", user, "-p", password]
        run_command(command)


def docker_image_tag(image, tag):
        command = ["sudo", "docker", "rmi", tag]
        run_command(command)
	command = ["sudo", "docker", "tag", image , tag]
        run_command(command)
        
def add_dockerImage(image):

        client = docker.from_env()
        cli = docker.APIClient(base_url='unix://var/run/docker.sock')
        for line in cli.push(image, stream=True, decode=True):
		line              
        #print("Image added successfully")


if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
	project_name= str(sys.argv[4])
        docker_image = str(sys.argv[5])
        tag = r'{}/{}/{}:latest'.format(harbor_host, project_name, str(sys.argv[6]))
        docker_login(harbor_host, user, password)
        docker_image_tag(docker_image,tag)
        add_dockerImage(tag)
 
        
       	 

