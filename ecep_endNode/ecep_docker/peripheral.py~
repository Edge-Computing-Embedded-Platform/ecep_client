"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
This is to interface between container and
host device access. 
"""
from docker import Client
import requests
from requests.exceptions import HTTPError
import json


class peripherelAcess:
    def container_peripherelAccess(self, **kwargs):
        """
        - API creates container and also provides peripherel access.
        - API is equivalent to create container with host configurations added to it.
        - Response
        """
        host_config = {}
        # image = kwargs['image']
        # network_disabled = kwargs['network_disabled']
        # host_config = {'devices': '/sys/class/leds:/:rwm'}

        # print image,host_config
        invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.18')

        containerID = invoke_clientAPI.create_container(
            'ubuntu', 'true', stdin_open=bool('True'), command=list['/bin/bash'],
            host_config=invoke_clientAPI.create_host_config(devices=['/dev/sda:rwm']))

        # containerID = invoke_clientAPI.create_container(image)
        return containerID


if __name__ == "__main__":
    obj = peripherelAcess()
    params = {'ports': '1000', 'image': 'tej', 'name': 'ecep', 'network_disabled': 'True'}
    ID = obj.container_peripherelAccess(**params)
    print ID
