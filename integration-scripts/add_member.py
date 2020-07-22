#!/usr/bin/python

try:
    import docker
    import request
    import sys
    import time
    import json
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import requests
    import sys
    import time
    import json

def get_project_id(project_name):

        resp = requests.get(r'https://{}/api/v2.0/projects?name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        if resp.status_code != 200:
    # if something went wrong.
                print('Error fetching project with name "{}"  /api/projects {}'.format(project_name,resp.status_code))

        resp_dump = json.dumps(resp.text)
        resp_str = json.loads(resp_dump)
	return [resp_str[24:35].split(',', 1)[0]]


def add_member(project_name,user_name):
	project_details = get_project_id(project_name)
	project_id = int(project_details[0])
        add_member = {
  "role_id": 2,
  "member_group": {
    "group_name": "string",
    "ldap_group_dn": "string",
    "group_type": 0,
    "id": 0
  },
  "member_user": {
    "username": user_name,
    "user_id": 0
  }
}

        resp = requests.post(r'https://{}/api/v2.0/projects/{}/members'.format(harbor_host,project_id), json=add_member,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 201:
                print('Error adding member to project ! POST error with status code /api/projects {}'.format(resp.status_code))
                return
        #print(r'{} Member successfully added'.format(user_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
        project_name = str(sys.argv[4])
	user_name = str(sys.argv[5])
        add_member(project_name,user_name)
       	 
