#!/usr/bin/python

try:
    import docker
    import request
    import sys
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import requests
    import sys


def create_project(project_name):
        create_project = {
  "count_limit": -1,
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
  "storage_limit": -1,
  "metadata": {
    "enable_content_trust": "false",
    "auto_scan": "false",
    "severity": "none",
    "reuse_sys_cve_whitelist": "false",
    "public": "false",
    "prevent_vul": "true"
  }
}

        resp = requests.post(r'https://{}/api/v2.0/projects'.format(harbor_host), json=create_project,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 201:
                print('Error creating project ! POST error with status code /api/projects {}'.format(resp.status_code))
                return
        #print(r'{} project successfully created'.format(project_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
        project_name = str(sys.argv[4])
        create_project(project_name)
       	 

