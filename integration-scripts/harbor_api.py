#Operations to create new projects and add a image into it 

try:
    import docker
    import sys
    import time
    import subprocess
    import requests
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import requests
    import sys
    import time
    import subprocess

#Inputs to be obtained from Hopsworks
harbor_host='10.0.2.15:30003'
user='admin'
password='Harbor12345'
project_name = 'kube-project'
docker_image = 'docker.io/registry:2'
tag = r'{}/{}/{}:latest'.format(harbor_host, project_name, 'registry')

def run_command(command):
    print "Command: ", subprocess.list2cmdline(command)
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise Exception('Error: Exited with error code: {}. Output:{}'.format(e.returncode, e.output))
    return output


def get_projects():

	resp = requests.get(r'https://{}/api/projects'.format(harbor_host),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
	if resp.status_code != 200:
    # if something went wrong.
    		print('GET /api/projects {}'.format(resp.status_code))
	print(resp.json())


def create_project(project_name,count_limit,storage_limit): 
	create_project = {
  "count_limit": count_limit,
  "project_name": project_name,
  "cve_whitelist": {
    "items": [
      {
        "cve_id": ""
      }
    ],
    "project_id": 0,
    "id": 0,
    "expires_at": 0
  },
  "storage_limit": storage_limit,
  "metadata": {
    "enable_content_trust": "false",
    "auto_scan": "false",
    "severity": "none",
    "reuse_sys_cve_whitelist": "false",
    "public": "false",
    "prevent_vul": "true"
  }
}
	resp = requests.post(r'https://{}/api/projects'.format(harbor_host), json=create_project,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
	if resp.status_code != 201:
    		print('POST /api/projects {}'.format(resp.status_code))
	print(r'{} successfully created'.format(project_name))



def docker_login(harbor_host, user, password):
	command = ["sudo", "docker", "login", harbor_host, "-u", user, "-p", password]
    	print ("Docker Login Command Running ")
    	print(run_command(command))


def docker_image_tag(image, tag):
	command = ["sudo", "docker", "tag", image , tag]
	print(run_command(command))
	print("Image successfully tagged")

def add_dockerImage(image): 

	client = docker.from_env()
	cli = docker.APIClient(base_url='unix://var/run/docker.sock')
	print("Pushing image...")
	for line in cli.push(image, stream=True, decode=True):
		print(line)
	print("Image added successfully")
	

docker_login(harbor_host, user, password)
get_projects()
create_project(project_name,-1,-1)
docker_image_tag(docker_image,tag)
add_dockerImage(tag)

