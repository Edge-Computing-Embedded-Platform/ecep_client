"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

This is to interface between Wamp client and
container API. 
"""

from ..ecep_docker import container, addFile_toContainer
from deviceRegister import sendResponse
from fetcher import *

# Call appropriate functions according to the commands received from user
def callContainer(data):
    """
    Calls the particular container API.
    """
    
    #print (data)

    # Form the response packet to be sent back to server
    response = data
    
    # restructure the received commands according to the API calls
    cmd = {}

    # To create a container
    if data['command'] == 'create':
        cmd['name'] = data['containerName']
        cmd['image'] = data['imageName']
        response['ID'] = container.create_containers(cmd)
        
        if response['ID'] == None:
            response['status'] = 'create failed'
        else:
            response['status'] = 'created'
        

    # To remove a container
    if data['command'] == 'remove':
        cmd['container'] = data['containerName']
        response['success'] = container.delete_container(cmd)
        
        if response['success']:
            response['status'] = 'removed'
        else:
            response['status'] = 'remove failed'

    # To start a container
    if data['command'] == 'start':
        cmd['container'] = data['containerName']
        response['success'] = container.run_container(cmd)
        
        kwargs = {'username' : data['containerName'].split('_')[0], 'containerName' :
            data['containerName'].split('_')[1], 'filename' : data['filename']}
        cmd['local_path'] = fetcher.get_file(**kwargs)
        
        execFile = addFile_toContainer.addFile()
        response['success'] = execFile.copyFileTo_container(cmd)
        
        if response['success']:
            response['status'] = 'started'
        else:
            response['status'] = 'start failed'
        

    # To stop a container
    if data['command'] == 'stop':
        cmd['container'] = data['containerName']
        response['success'] = container.stop_container(cmd)
        
        if response['success']:
            response['status'] = 'stopped'
        else:
            response['status'] = 'stop failed'
            
    sendResponse(response)
    
    
def getContainerList():
    """
    Gets a list of containers running / created / stopped.
    """
    contList = []
    containerInfo = {}
    args = {'all':'all'}
    contListRaw = container.list_containers(args)
    
    for entries in contListRaw:
        containerInfo['status'] = entries['State']
        containerInfo['info'] = entries['Status']
        containerInfo['containerName'] = entries['Names']
        containerInfo['ID'] = entries['Id']
        
        contList.append(containerInfo.copy())
        
    return contList
        
