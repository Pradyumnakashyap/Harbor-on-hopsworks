#!/usr/bin/python

 #Operations delete users from projects 

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
	return [resp_str[24:35].split(',', 1)[0]]

	

def get_member_id(project_id,user_name):
	resp = requests.get(r'https://{}/api/v2.0/projects/{}/members?entityname={}'.format(harbor_host,project_id,user_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        if resp.status_code != 200:
    # if something went wrong.
        	print('Error fetching member in the project  with name "{}"  /api/projects {}'.format(user_name,resp.status_code))

        resp_dump = json.dumps(resp.text)
        resp_str = json.loads(resp_dump)
        return [resp_str[16:22].split(',', 1)[0]]


def delete_member(project_name,user_name):

        project_detail = get_project_id(project_name)
	project_id = int(project_detail[0])
	print(project_id)
	member_detail = get_member_id(project_id,user_name)
	member_id = int(member_detail[0])
	print(member_id)
        if member_id > 0:
               	resp = requests.delete(r'https://{}/api/v2.0/projects/{}/members/{}'.format(harbor_host,project_id,member_id),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
               	if resp.status_code != 200:
               		print('Error deleting member from project ! POST error with status code /api/projects {}'.format(resp.status_code))
			return
        #print(r'{} Member successfully deleted'.format(user_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
        project_name = str(sys.argv[4])
	user_name = str(sys.argv[5])
        delete_member(project_name,user_name)
