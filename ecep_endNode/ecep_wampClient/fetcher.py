"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
"""

import urllib2
import json
import os
ip = "ec2-52-39-130-106.us-west-2.compute.amazonaws.com"
port = 9000
route = '/download'
file_root_path = None

def init_fetcher(root_path):
    global file_root_path
    if file_root_path is None:
        file_root_path = root_path

def get_file(**kwargs):
    key = ['username', 'containerName', 'filename']
    print kwargs
    for param in key:
        if param not in kwargs:
            raise ValueError("Missing %s" % param)
	

    url = 'http://' + ip + ':' + str(port) + route
    print url

    try:
        data = json.dumps(kwargs)
        headers = {'Content-Type': 'application/json'}
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        print  file_root_path + kwargs['username'] + "_" + kwargs['containerName'] + '/' + kwargs['filename']

        file_path = file_root_path + kwargs['username'] + "_" + kwargs['containerName'] + '/' + kwargs['filename']
        local_path = file_root_path + kwargs['username']+'_'+kwargs['containerName']
        if not os.path.exists(file_root_path + kwargs['username']+'_'+kwargs['containerName']):
            os.makedirs(file_root_path + kwargs['username']+'_'+kwargs['containerName'])

        print(file_path)
        with open(file_path, 'wb') as output:
            while True:
                chunk = response.read(2048)
                if not chunk:
                    break
                output.write(chunk)
                print "downloading"
                output.flush()
        return file_path
    except Exception, e:
            print(e)

if __name__  == "__main__":

    data = {'username':'admin','containerName':'pull','filename':'Doc1.docx'}
    get_file(**data)


