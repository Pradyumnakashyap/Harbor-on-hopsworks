#!/usr/bin/python

try:
    import docker
    import request
    import sys
    import time
    import subprocess
    import requests
    import json
    import datetime

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
    import datetime

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
        #command = ["sudo", "docker", "rmi", tag]
        #intermediate= run_command(command)
	command = ["sudo", "docker", "tag", image , tag]
        run_command(command)
        
def add_dockerImage(image):

        client = docker.from_env()
        cli = docker.APIClient(base_url='unix://var/run/docker.sock')
        for line in cli.push(image, stream=True, decode=True):
		line              
        command = ["sudo", "docker", "rmi", tag]
        run_command(command) #Delete local image upon push
	#print("Image added successfully")


if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
	project_name= str(sys.argv[4])
        docker_image = str(sys.argv[5])
	now = datetime.datetime.now()
	dt_string = now.strftime("%d%m%Y%H%M")
        tag = r'{}/{}/{}:{}'.format(harbor_host, project_name, 'conda-image',dt_string)
        docker_login(harbor_host, user, password)
        docker_image_tag(docker_image,tag)
        add_dockerImage(tag)
 
        
       	 

