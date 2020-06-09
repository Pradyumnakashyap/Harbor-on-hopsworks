#Operations to create new projects and add a image into it 

try:
    import docker
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
    import subprocess
    import json


def run_command(command):
    print "Command: ", subprocess.list2cmdline(command)
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise Exception('Error: Exited with error code: {}. Output:{}'.format(e.returncode, e.output))
    return output

def get_project_id(project_name):

        resp = requests.get(r'https://{}/api/projects?name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        if resp.status_code != 200:
    # if something went wrong.
                print('Error fetching project with name "{}"  /api/projects {}'.format(project_name,resp.status_code))

        resp_dump = json.dumps(resp.text)
        resp_str = json.loads(resp_dump)
        return [resp_str[24], resp_str[301]]

def docker_login(harbor_host, user, password):
        command = ["sudo", "docker", "login", harbor_host, "-u", user, "-p", password]
        print ("Docker Login Command Running ")
        print(run_command(command))

def delete_repo(project_name):

        repo_name = r'{}/{}'.format(project_name,'conda_image')
        resp = requests.delete(r'https://{}/api/repositories/{}/tags/{}'.format(harbor_host,repo_name,'latest'),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
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
                resp = requests.delete(r'https://{}/api/projects/{}'.format(harbor_host,project_detail[0]),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
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
        project_name = 'kube-test'
        docker_login(harbor_host, user, password)
        delete_project(project_name)

