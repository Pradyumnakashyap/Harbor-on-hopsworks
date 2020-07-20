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
        return [resp_str[24], resp_str[301]]

def delete_repo(project_name):

        repo_name = r'{}/{}'.format(project_name,'busybox')
        resp = requests.delete(r'https://{}/api/v2.0/projects/{}/repositories/{}:{}'.format(harbor_host,project_name,repo_name,'latest'),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 200:
                print('Error deleting the repository with status code /api/projects {}'.format(resp.status_code))
                return 0
        return 1

def delete_project(project_name):

        repo_flag = 1
        project_detail = get_project_id(project_name)
        if project_detail[1] > 0:
                repo_flag = delete_repo(project_name)
        if repo_flag:
                resp = requests.delete(r'https://{}/api/v2.0/projects/{}'.format(harbor_host,project_detail[0]),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
                if resp.status_code != 200:
                        print('Error Deleting with status code /api/projects {}'.format(resp.status_code))
                        return
                print('Project successfully deleted')
        else:
                print('Error deleting project {}'.format(project_name))

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        harbor_host='10.0.2.15:30003'
        user='admin'
        password='Harbor12345'
        project_name='kube-test'
        delete_project(project_name)

