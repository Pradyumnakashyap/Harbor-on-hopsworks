#Operations to create new projects and add a image into it 
#curl command - curl -u admin:Harbor12345 -i -k -X GET "https://10.0.2.15:30003/api/projects"

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

def run_command(command):
    print "Command: ", subprocess.list2cmdline(command)
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise Exception('Error: Exited with error code: %s. Output:%s'% (e.returncode, e.output))
    return output


def get_projects():

	resp = requests.get('https://10.0.2.15:30003/api/projects',verify='/etc/docker/certs.d/10.0.2.15:30003/ca.crt',auth=('admin','Harbor12345'))
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
	resp = requests.post('https://10.0.2.15:30003/api/projects', json=create_project,verify='/etc/docker/certs.d/10.0.2.15:30003/ca.crt',auth=('admin','Harbor12345'),headers={'Content-Type':'application/json'})
	if resp.status_code != 201:
    		print('POST /api/projects {}'.format(resp.status_code))
	print('Successfully created ')



def docker_login(harbor_registry, user, password):
	command = ["sudo", "docker", "login", harbor_host, "-u", user, "-p", password]
    	print "Docker Login Command: ", command
    	run_command(command)

def docker_image_tag(image, harbor_registry, tag = None):
	_tag = 'latest'
	if tag is not None:
	    _tag = tag
	try:
	    cli.tag(image, harbor_registry, _tag, force=True)
	    return harbor_registry, _tag
	except docker.errors.APIError, e:
	    raise Exception(r" Docker tag image {} failed, error is [{}]".format (image, e.message))

def add_dockerImage(): 

	client = docker.from_env()
	cli = docker.APIClient(base_url='unix://var/run/docker.sock')
	
	


create_project('test',2,10)
