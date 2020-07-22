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

def create_user(user_name,user_password,email):
	user_details = {
  "username": user_name,
  "realname": user_name,
  "password": user_password,
  "email": email
}

	resp = requests.post(r'https://{}/api/v2.0/users'.format(harbor_host), json=user_details,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 201:
                print('Error creating a user in Harbor ! POST error with status code /api/projects {}'.format(resp.status_code))
                return
        #print(r'{} created user successfully'.format(user_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
	user_name = str(sys.argv[4])
	user_password = str(sys.argv[5])
	email = str(sys.argv[6])
        create_user(user_name,user_password,email)
