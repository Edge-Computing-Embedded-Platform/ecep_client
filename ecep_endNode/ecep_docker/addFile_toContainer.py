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
		print ('startConatiner')
		containerID = kwargs['container_name']
	        status = {}
		
		try:
			response = invoke_cli.start(containerID)
			status["status"] = "True"
		except:
			status["status"] = "False"
		
		return json.dumps(status)
			

	def copyFileTo_container(self, **kwargs):
		print ('copyFile routine')
		global filetype, containerID, user
		containerID = kwargs['container_name']	
		path = kwargs['containerpath']
		data = kwargs['file']
		localpath = kwargs['local_path']
		
		try:
			get_fileObj = open(localpath)
		except OSError as err:
			print err.errno == errno.EPERM
			
		filetype =  os.path.basename(localpath)
		print ('filetype: ',filetype)
		pw_tarstream = BytesIO()
		pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w') #class for reading and writing tar archives. 
		file_data = get_fileObj
		tarinfo = tarfile.TarInfo(name=filetype) #create an object
		tarinfo.size = os.path.getsize(localpath)
		tarinfo.mtime = time.time()
		pw_tar.addfile(tarinfo, get_fileObj)
		pw_tar.close()
		pw_tarstream.seek(0)
		
        	_putArchive_response = invoke_cli.put_archive(containerID,path,pw_tarstream)
        	print ('_putArchive_response: ',_putArchive_response)
        	
        	if _putArchive_response: 
        		_script = {'container_name': containerID, 'user':'root'}
        		print ('container_name: ',containerID) 
        		self.run_shellScript(**_script)
        		
        	return _putArchive_response
        	
        def run_shellScript(self, **kwargs):	
        	print('run_shell routine')	
		containerID = kwargs['container_name']	
		#print ('con_name: ',containerID)
		#stdout = kwargs['stdout']
		user = kwargs['user']
		exe_file = filetype
		print ('executableFile: ',exe_file)
		_file_location = os.path.join("/",exe_file)
		print _file_location
		cmmd = ['sh',_file_location]
		print ('containerID_shellroutine: ,user: ',containerID,user)
		response = invoke_cli.exec_create(container=containerID,cmd=cmmd,user='root')
		print ('response: ',response)
		ID = response
		response1 = invoke_cli.exec_start(exec_id = ID)
		print ('response1: ',response1) 
		

if __name__ == "__main__":
	obj = addFile()
	name = {'container_name' : 'nostalgic_bhabha'}
	obj.startContainer_toAddFile(**name)
	#time.sleep(10)
	data = {'container_name':'nostalgic_bhabha','containerpath':'/','local_path':'/home/parallels/hello.sh','file':'temp.tar'}
	obj.copyFileTo_container(**data)
	#time.sleep(5)
	#script = {'container_name':'nostalgic_bhabha','user':'root'}
	#obj.run_shellScript(**script)
        	
        	
