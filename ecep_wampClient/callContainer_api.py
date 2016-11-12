"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

This is to interface between Wamp client and
container API. 
"""

from ..ecep_docker import container
from deviceRegister import sendResponse

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
        response['status'] = 'created'
        

    # To remove a container
    if data['command'] == 'remove':
        cmd['container'] = data['containerName']
        response['success'] = container.delete_container(cmd)
        response['status'] = 'removed'

    # To start a container
    if data['command'] == 'start':
        cmd['container'] = data['containerName']
        response['success'] = container.run_container(cmd)
        response['status'] = 'started'
        

    # To stop a container
    if data['command'] == 'stop':
        cmd['container'] = data['containerName']
        response['success'] = container.stop_container(cmd)
        response['status'] = 'stopped'
        
    
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
        
