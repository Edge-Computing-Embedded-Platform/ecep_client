"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
"""

from docker import Client
import requests
from requests.exceptions import HTTPError
import json


def create_containers(args):
    """
    - API to create containers.
    - API is equivalent to docker run command.

    - Response if image is found locally:
      {u'Id': u'67d1f4f5fb5e667f03e55e3b794fe34b95304d0cec584459ca0f84fa3c0681e1', u'Warnings': None}
    - If image is not found locally, then it is pulled from docker hub and the response is a json string.

    - returns container ID if sucessful or None if unsuccessful
    """

    print ("In create container")
    #args['detach'] = ('True')
    if 'detach' in args:
        args['detach'] = bool(args['detach'])
    if 'stdin_open' in args:
        args['stdin_open'] = bool(args['stdin_open'])
    if 'name' in args:
        args['name'] = str(args['name'])
    if 'image' in args:
        args['image'] = str(args['image'])
    if 'tty' in args:
        args['tty'] = bool(args['tty'])
    if 'network_disabled' in args:
        args['network_disabled'] = bool(args['network_disabled'])
        
    #print ('detach: ',args['detach'])

    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')

    try:
        containerID = invoke_clientAPI.create_container(**args)
        print ('container ID: ', containerID)
        print ('IN FIRST TRY CALL')
        print ('Created container in 1st try') 
        print ('Will start the container now')
    	start_container = invoke_clientAPI.start(container=containerID.get('Id'))
    except Exception as e:
        print ('IN FIRST Exception')
        print e
        try:
            for line in invoke_clientAPI.pull(args['image'], stream=True):
                print(json.dumps(json.loads(line), indent=4))
            # invoke_clientAPI.pull(args['image'],stream=True)

            containerID = invoke_clientAPI.create_container(**args)
            print ('Created container, but had to pull the image')
        except HTTPError:
            containerID = None
    
    """
        for line in invoke_clientAPI.pull(args['image'], stream=True):
                 print(json.dumps(json.loads(line), indent=4))


         #containerID = invoke_clientAPI.create_container(**args)
         #print ('CONTAINERID: ',containerID)
    """

    print containerID
    return containerID


def list_containers(args):
    """
    - API to list all running containers.
    - API is equivalent to docker ps command.

    - Response is a list of dictionary:
    [{u'Status': u'Up 25 minutes', u'Created': 1477874345, u'Image':
     u'sha256:2b786d1d393fca95d9baa72c40b7d2da8b4fc3135659b7ca3046967f8de09c15',
     u'Labels': {}, u'NetworkSettings': {u'Networks': {u'bridge': {u'NetworkID':
     u'f3211da5394d90c58365fb9f50285480735171ef88a4f21399ec08575797f21f',
     u'MacAddress': u'02:42:ac:11:00:02', u'GlobalIPv6PrefixLen': 0, u'Links': None,
     u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None,
     u'EndpointID': u'932507e69777dc1c9bd5784941d92722889a9d76af1a10672afb1c063c092398',
     u'IPPrefixLen': 16, u'IPAddress': u'172.17.0.2', u'Gateway': u'172.17.0.1',
     u'Aliases': None}}}, u'HostConfig': {u'NetworkMode': u'default'}, u'ImageID':
     u'sha256:2b786d1d393fca95d9baa72c40b7d2da8b4fc3135659b7ca3046967f8de09c15',
     u'State': u'running', u'Command': u'/bin/bash', u'Names': [u'/nostalgic_bhabha'],
     u'Mounts': [], u'Id': u'2b5c2b8de6610c2d443518a84ca7c56ded98fbcf9a70c02ea73746b5c05dd21e',
     u'Ports': []}]

    """

    if 'all' in args:
        args['all'] = bool(args['all'])
    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    container_list = invoke_clientAPI.containers(**args)
    return container_list


def run_container(args):
    """
    - API to run conatiners.
    - API is equivalent to docker start command.

    - Response is in dict form:
        Format: {'container':'container_name'}
        Returns 'Success' if container starts successfully if not 'Failed'
    """
    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='auto')
    container_ID = {}
    container_ID = {'container': args['container']}
    status = {}
    try:
        start_container = invoke_clientAPI.start(**container_ID)
        status["status"] = "True"
    except:
        status["status"] = "False"
        
    return json.dumps(status)


def delete_container(args):
    """
    - API to remove container
    - API is equivalent to docker rm cmd

    - Response is in dict:
        Format: {'container': 'container_name'}
        Returns 'Success' if container is deleted successfully if not 'Failed'
    """
    if 'container' in args:
        args['container'] = str(args['container'])
    if 'v' in args:
        args['v'] = bool(args['v'])
    if 'link' in args:
        args['link'] = bool(args['link'])
    if 'force' in args:
        args['force'] = bool(args['force'])

    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    status = {}
    try:
        container_removed = invoke_clientAPI.remove_container(**args)
        status["status"] = "True"
    except:
        status["status"] = "False"
        
    return json.dumps(status)
    

def delete_image(args):
    """
    - API to remove Image.
    - API is equivalent to docker rmi cmd.

    - Response is in dict:
        Format: {'force':'force','image':'Image_name'}
        Returns 'Success' if container is removed successfully if not 'Failed'.
    """
    if 'image' in args:
        args['image'] = str(args['image'])
    if 'force' in args:
        args['force'] = bool(args['force'])
    if 'noprune' in args:
        args['noprune'] = bool(args['noprune'])

    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    status = {}
    try:
        image_removed = invoke_clientAPI.remove_image(**args)
        status["status"] = "True"
    except:
        status["status"] = "False"
        
    return json.dumps(status)


def stop_container(args):
    """
    - API to stop container
    - API is equivalent to docker stop cmd

    - Response is in dict:
            Format: {'container': 'container_name'}
        Returns 'Success' if container starts successfully if not 'Failed'
    """
    if 'container' in args:
        args['container'] = str(args['container'])
    if 'timeout' in args:
        args['timeout'] = bool(args['stop'])

    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    status = {}
    try:
        halt_container = invoke_clientAPI.stop(**args)
        status["status"] = "True"
    except:
        status["status"] = "False"
    
    return json.dumps(status)


def rename_container(args):
    """
    - API to rename container
    - API is equivalent to docker rename

    - Response is in dict:
        Format : {'container': 'oldContainer_name', 'name': 'newContainer_name'}
        Returns 'Success' if container is renamed successfully if not 'Failed'
    """
    if 'ID' in args:
        args['ID'] = str(args['ID'])
    if 'name' in args:
        args['name'] = str(args['name'])

    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.18')
    status = {}
    try:
        newname_container = invoke_clientAPI.rename(**args)
        status["status"] = "True"
    except:
        status["status"] = "False"
        
    return json.dumps(status)

####Testing purposes##################
# cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
# container = cli.create_container(image='busybox:latest', command='/bin/sleep 30')
# print(container)
