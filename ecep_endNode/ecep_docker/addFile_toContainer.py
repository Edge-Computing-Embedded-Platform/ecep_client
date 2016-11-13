"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

This is to interface between Wamp client and
container API. 
"""
from docker import Client
from io import BytesIO
import json
import os
import tarfile
import time

invoke_cli = Client(base_url='unix://var/run/docker.sock')

class addFile:
	def startContainer_toAddFile(self, **kwargs):
		containerID = kwargs['container_name']
	        response = invoke_cli.start(containerID)
	        print (response)

	def copyFileTo_container(self, **kwargs):
		print kwargs
		if kwargs is not None:
			for key, value in kwargs .iteritems():
				print "%s == %s" %(key,value)
			
		containerID = kwargs['container_name']	
		path = kwargs['filepath']
		data = kwargs['file']
		localpath = kwargs['local_path']
		
		try:
			admin_password = open(localpath)
		except OSError as e:
			print e.errno == errno.EPERM
			
		filetype =  os.path.basename(localpath)
		pw_tarstream = BytesIO()
		pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w') #class for reading and writing tar archives. 
		file_data = admin_password
		tarinfo = tarfile.TarInfo(name=filetype) #create an object
		tarinfo.size = os.path.getsize(localpath)
		tarinfo.mtime = time.time()
		pw_tar.addfile(tarinfo, admin_password)
		pw_tar.close()
		pw_tarstream.seek(0)
		
		print containerID, path, data
        	response = invoke_cli.put_archive(containerID,path,pw_tarstream)
        	print (response)
        	
        def run_shellScript(self, **kwargs):
        	print kwargs
        	if kwargs is not None:
			for key, value in kwargs .iteritems():
				print "%s == %s" %(key,value)
		print kwargs
		containerID = kwargs['container_name']	
		#stdout = kwargs['stdout']
		user = kwargs['user']
		cmmd = ['sh','/hello.sh']
		print containerID,user
		response = invoke_cli.exec_create(container='nostalgic_bhabha',cmd=cmmd,user='root')
		print response1
		ID = response1
		response = invoke_cli.exec_start(exec_id = ID)
		print response 
		

if __name__ == "__main__":
	obj = addFile()
	name = {'container_name' : 'nostalgic_bhabha'}
	obj.startContainer_toAddFile(**name)
	#time.sleep(10)
	data = {'container_name':'nostalgic_bhabha','filepath':'/','local_path':'/home/parallels/hello.sh','file':'temp.tar'}
	obj.copyFileTo_container(**data)
	#time.sleep(5)
	script = {'container_name':'nostalgic_bhabha','user':'root'}
	obj.run_shellScript(**script)
        	
        	
