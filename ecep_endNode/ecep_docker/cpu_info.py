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
    location = "unknown"
    send_url = 'http://freegeoip.net/json'

    for i in range(5):
        try:
            r = requests.get(send_url, )

            j = json.loads(r.text)
            lat = j['latitude']
            lon = j['longitude']
            city = j['city']
            state = j['region_name']
            location = city + ', ' + state
        except Exception, e:
            continue

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
    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    try:

        info = invoke_clientAPI.info()

        key = ('Containers', 'Images', 'KernelVersion', 'OperatingSystem', 'NCPU', 'Name')
        ret = dict((value, info[value]) for value in key)

        ret['deviceName'] = ret.pop('Name')
        ret['totalContainers'] = ret.pop('Containers')
        ret['totalImages'] = ret.pop('Images')
        ret['kernelVersion'] = ret.pop('KernelVersion')
        ret['os'] = ret.pop('OperatingSystem')
        ret['CPUs'] = ret.pop('NCPU')

        # CPU percentage
        ret['CPUUsage'] = psutil.cpu_percent(interval=2.0)

        # Get the RAM info
        mem = psutil.virtual_memory()
        ret['physicalMem'] = convertToMB(mem.total)
        ret['physicalUsed'] = convertToMB(mem.used)
        ret['physicalPercent'] = mem.percent
        ret['physicalUnused'] = convertToMB(mem.available)

        # Get the Disk memory info
        mem = psutil.disk_usage('/')
        ret['diskMem'] = converToGB(mem.total)
        ret['diskUsed'] = converToGB(mem.used)
        ret['diskPercent'] = mem.percent
        ret['diskUnused'] = converToGB(mem.free)

    except Exception as e:
        ret = None

    return ret


def getCpuName():
    """
    Name of the CPU is fetched
    """
    invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    try:

        info = invoke_clientAPI.info()
        name = info['Name']

    except Exception as e:
        name = None

    return name


if __name__ == '__main__':
    """
    For testing
    """
    print ('The machine is: ', getMachineArchitecture())
    print('The location of the device is: ', getDeviceLocation())
    print(getCpuInfo())
    print(getCpuName())
