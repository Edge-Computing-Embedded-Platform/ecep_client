"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

Registers the device with a unique name, periodic 
heartbeat message generation and transmit other 
messages such as logs, etc.
"""

import threading
import time
import sys
from wamp_client import *
import callContainer_api as cca

from ..ecep_docker import cpu_info

ticks = 5

# decorator for threads
def threaded(func):
    """
    A wrapper to create a thread.
    Takes function as input.
    Returns a handler for thread.
    """
    def func_wrapper(*args, **kwargs):
        thread = threading.Thread(target = func, args = args, kwargs = kwargs)
        thread.setDaemon(True)
        thread.start()
        return thread
    return func_wrapper


class periodicTransmit(object):
    """
    This class definitions which handle message
    transmission.
    """
    
    def __init__(self, deviceID):
        self._deviceId = deviceID
        self._topic = None
        self._heartbeatData = {}
        self._containerData = {}
    
    #device registration and heartbeat
    @threaded
    def heartbeat(self):
        while True:
            self._topic = "com.ecep.heartbeat"
            self._heartbeatData['deviceId'] = self._deviceId
            self._heartbeatData['location'] = cpu_info.getDeviceLocation()
            self._heartbeatData['arch'] = cpu_info.getMachineArchitecture()
            sendTo(self._topic, self._heartbeatData)
            
            print("topic: " +self._topic+ ", data: ")
            print(self._heartbeatData)
            time.sleep(ticks)
            
    #Send container status
    @threaded
    def containerStatus(self):
        while True:
            self._topic = "com.ecep.containerStatus"
            self._containerData['deviceId'] = self._deviceId
            self._containerData['contList'] = cca.getContainerList()
            sendTo(self._topic, self._containerData)
            
            print ('number of containers = ',  len(self._containerData['contList']))
            print("topic: " +self._topic+ ", data: " )
            print(self._containerData)
            time.sleep(ticks*10)
            
            
    #Send CPU information
    @threaded
    def cpuInfo(self):
        while True:
            self._topic = "com.ecep.cpuInfo"
            self._cpuInfo['deviceId'] = self._deviceId
            self._cpuInfo = cpu_info.getCpuInfo()
            
            
            
def sendResponse(response):
    """
    This sends out the response from the execution of
    container commands to the server.
    """
    topic = "com.ecep.deviceResponse"
    data = response
    sendTo(topic, data)
            
            
if __name__ == "__main__":
     
    device = 'beaglebone'
    
    # params for wampserver
    ip = sys.argv[1]
    port = sys.argv[2]
    realm = sys.argv[3]

    print(ip, port, realm)
    while True:
        time.sleep(5)
    
    client = wampserver(device)
    check = client.connect(ip, port, realm)
    
    #wait till the connection is established
    time.sleep(10)
    
    #create an instance
    periodicTransmit_I = periodicTransmit(device)
    
    # Launch thread
    handle_heartbeat = periodicTransmit_I.heartbeat()
    handle_containerStatus = periodicTransmit_I.containerStatus()
    
    while True:
        time.sleep(2)
        
    handle_heartbeat.join()
    handle_containerStatus.join()
