"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
"""


#### This code gives brief info about CPU utilization ###
### Uses platform and psutil libraries ###
### Modifications to be made ###

import platform
import psutil
import requests
import json


def getMachineArchitecture():
    """
    gets the architecture of the machine
    """
    return platform.machine()
    
    
def getDeviceLocation():
    """
    queries the device location
    """
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    city = j['city']
    state = j['region_name']
    
    location = city + ', ' + state
    return location

    
print (platform.version())
print (platform.platform())
print (platform.uname())
print (platform.system())
print (platform.processor())


print (psutil.cpu_times())
print (psutil.virtual_memory())
print (psutil.disk_partitions())

