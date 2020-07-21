#!/usr/bin/python

 #Operations delete projects  

try:
    import docker
    import sys
    import time
    import requests
    import json

except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import requests
    import json

def get_project_id(project_name):

        resp = requests.get(r'https://{}/api/v2.0/projects?name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        if resp.status_code != 200:
    # if something went wrong.
                print('Error fetching project with name "{}"  /api/projects {}'.format(project_name,resp.status_code))

        resp_dump = json.dumps(resp.text)
        resp_str = json.loads(resp_dump)
	return [resp_str[24:35].split(',', 1)[0], resp_str[299:310].split(',', 1)[0]]

def delete_repo(project_name):

        repo_name="conda-image"
        resp = requests.delete(r'https://{}/api/v2.0/projects/{}/repositories/{}'.format(harbor_host,project_name,repo_name),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 200:
                print('Error deleting the repository with status code /api/projects {}'.format(resp.status_code))
                return 0
        return 1

def delete_project(project_name):

        try:
		repo_flag = 1
        	project_detail = get_project_id(project_name)
        	if int(project_detail[1]) > 0:
                	repo_flag = delete_repo(project_name)
        	if repo_flag :
                	resp = requests.delete(r'https://{}/api/v2.0/projects/{}'.format(harbor_host,int(project_detail[0])),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
                	if resp.status_code != 200:
                        	print('Error deleting project with status code /api/projects {}'.format(resp.status_code))
                        	return
                #print('Project successfully deleted')
       	 	else:
                	print('Error deleting project {}'.format(project_name))
	except ValueError as e:
      		print (r'Project with the name {} does not exist!'.format(project_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
	user = str(sys.argv[2])
        password= str(sys.argv[3])
        project_name=str(sys.argv[4])
        delete_project(project_name)
      

