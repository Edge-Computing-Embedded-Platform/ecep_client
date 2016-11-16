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
	"""
	This class definitions handle transferring a file into containers and executing them inside a container. 
	"""
	def __init__(self):
		self._containerName = None
		self._localPath = None
		self._containerPath = None
		self._shellPath = os.path.dirname(os.path.realpath(__file__))
		self._user = 'root'
		self._fileType = None
		self._status = {}
		self._command = []
		self._file = None
		self._count = 1
		
	def startContainer_toAddFile(self, **kwargs):
		"""
		Starts a container to setup the file transfer.
		"""
		print ('startConatiner')
		self._containerName = kwargs['container_name']
		
		try:
			response = invoke_cli.start(self._containerName)
			self._status["status"] = "True"
		except:
			self._status["status"] = "False"
		
		return json.dumps(self._status)
			
	#def transferFile(self,**kwargs):
		

	def copyFileTo_container(self, **kwargs):
		"""
		Copies a file to container. 
		"""
		print ('copyFile routine')
		self._containerName = kwargs['container_name']	
		self._containerPath = kwargs['containerpath']
		self._localPath = kwargs['local_path']
		
		if self._count == 0:
			print ('containerName: ,containerPath: ,localPath: ',self._containerName,self._containerPath,self._localPath)
		
		try:
			_fileObj = open(self._localPath)
		except OSError as err:
			print err.errno == errno.EPERM
			
		self._fileType =  os.path.basename(self._localPath)
		print ('filetype: ',self._fileType)
		
		"""
		if self._fileType.endswith("tar"):
			self.unTar_tar(self._localPath)
		elif self._fileType.endswith("tar.gz"):
			self.unTar_tarGz(self._localPath)
		else:
			print ('Unknow file type') 
		"""	
		_pw_tarstream = BytesIO()
		_pw_tar = tarfile.TarFile(fileobj=_pw_tarstream, mode='w') #class for reading and writing tar archives. 
		_tarinfo = tarfile.TarInfo(name=self._fileType) # ---> should be changed #create an object 
		_tarinfo.size = os.path.getsize(self._localPath)
		_tarinfo.mtime = time.time()
		_pw_tar.addfile(_tarinfo, _fileObj)
		_pw_tar.close()
		_pw_tarstream.seek(0)
		
        	_putArchive_response = invoke_cli.put_archive(self._containerName,self._containerPath,_pw_tarstream)
        	print ('_putArchive_response: ',_putArchive_response)
        	
        	if ((_putArchive_response) and (self._count == 1)): 
        		_script = {'container_name': self._containerName, 'user':self._user,'containerpath':'/'}
        		print ('container_name: ,count: ',self._containerName,self._count)  
        		self.run_shellScript(**_script)
        		
        	if((_putArchive_response) and (self._count == 0)):
        		_script = {'container_name': self._containerName, 'user':self._user}
        		print ('container_name: ,count: ',self._containerName,self._count) 
        		self.run_shellScript(**_script)
        		
        	return _putArchive_response
        	
        def run_shellScript(self, **kwargs):
        	"""
        	Executes the transferred file.
        	"""	
        	print('run_shell routine')	
		self._containerName = kwargs['container_name']	
		self._user = kwargs['user']
		
		
		if self._count == 1:
			self._count = 0
			self._containerName = kwargs['container_name']	
			self._containerPath = kwargs['containerpath']
			self._localPath = os.path.join(dir_path,'untar.sh')
			print self._localPath
			
			_shellscript = {'container_name': self._containerName, 'containerpath': self._containerPath,'local_path': self._localPath}
			self.copyFileTo_container(**_shellscript)
			#self._localPath = kwargs['local_path']
			

		_execFile = self._fileType
		#_execFile = untar.sh
		print ('executableFile: ',_execFile)
		_fileLocation_inContainer = os.path.join("/",_execFile)
		print ('_fileLocatio_inContainer: ',_fileLocation_inContainer)
		self._command = ['sh',_fileLocation_inContainer]
		print ('containerID_shellroutine: ,user: ',self._containerName,self._user)
		_execCreate_response = invoke_cli.exec_create(container=self._containerName,cmd=self._command,user=self._user)
		print ('_execCreate_response: ',_execCreate_response)
		_execStart_response1 = invoke_cli.exec_start(exec_id = _execCreate_response)
		print ('_execStart_response1: ',_execStart_response1) 
	
	"""
	def unTar_tarGz(self,tarGz_file):
		print ('untar tar.gz')
		tarGz_file.endswith("tar.gz")
		tar = tarfile.open(tarGz_file, "r:gz")
		tar.extractall()
		tar.close()
		_script = {'container_name': self._containerName, 'user':self._user}
		print ('container_name: ',self._containerName)
		self.run_shellScript(**_script)
		
	def unTar_tar(self,tarFile):
		print ('In untar .tar routine')
		print ('tarfile: ',tarFile)
		tarFile.endswith("tar")
		tar = tarfile.open(tarFile, "r:")
		tar.extractall()
		tar.close()
		_script = {'container_name': self._containerName, 'user':self._user}
		print ('container_name: ',self._containerName)
		self.run_shellScript(**_script)
	"""

if __name__ == "__main__":
	
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print dir_path
	
	
	obj = addFile()
	name = {'container_name' : 'nostalgic_bhabha'}
	obj.startContainer_toAddFile(**name)
	#time.sleep(10)
	data = {'container_name':'nostalgic_bhabha','containerpath':'/','local_path':'/home/parallels/Downloads/for_testing.tar','file':'temp.tar'}
	obj.copyFileTo_container(**data)
	#data1 = {'container_name':'nostalgic_bhabha','containerpath':'/','local_path':'/home/parallels/proj_295B/untar.sh','file':'temp.tar'}
	#obj.copyFileTo_container(**data1)
	#time.sleep(5)
	#script = {'container_name':'nostalgic_bhabha','user':'root'}
	#obj.run_shellScript(**script)

