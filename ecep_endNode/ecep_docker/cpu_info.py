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
from docker import Client
from collections import OrderedDict


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
    
    
def convertToMB(arg):
    return arg / float(1024 * 1024)
    
def converToGB(arg):
    return convertToMB(arg) / float(1024)
    
def getCpuInfo():
    """
    - API to get cpu info 
    - Response is in JSON format
    """
    print ("In cpu info")
    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock',version='1.12')
    try:
        
        info = invoke_clientAPI.info()
        
        key = ('Containers', 'Images', 'KernelVersion', 'OperatingSystem', 'NCPU', 'Name')
        ret = OrderedDict((value, info[value]) for value in key)
        
        ret['No. of Containers'] = ret.pop('Containers')
        ret['No. of Images'] = ret.pop('Images')
        ret['Kernel Version'] = ret.pop('KernelVersion')
        ret['Operating System'] = ret.pop('OperatingSystem')
        ret['No. of CPUs'] = ret.pop('NCPU')
        
        # CPU percentage
        ret['CPU percentage (%)'] = psutil.cpu_percent(interval = 2.0)
        
        # Get the RAM info
        mem = psutil.virtual_memory()
        ret['Total Memory (Mb)'] = convertToMB(mem.total)
        ret['Used Memory (Mb)'] = convertToMB(mem.used)
        ret['Percentage of Memory Usage (%)'] = mem.percent
        ret['Available Memory (Mb)'] = convertToMB(mem.available)
        
        # Get the Disk memory info
        mem = psutil.disk_usage('/')
        ret['Total Disk Memory (Gb)'] = converToGB(mem.total)
        ret['Used disk Memory (Gb)'] = converToGB(mem.used)
        ret['Percentage of Disk Memory Usage (%)'] = mem.percent
        ret['Available Disk Memory (Gb)'] = converToGB(mem.free)
        
    except Exception as e:
        ret = None	
    
    return ret

    
   
if __name__ == '__main__':

    print ('The machine is: ', getMachineArchitecture())
    print('The location of the device is: ', getDeviceLocation())
    print(getCpuInfo())
        