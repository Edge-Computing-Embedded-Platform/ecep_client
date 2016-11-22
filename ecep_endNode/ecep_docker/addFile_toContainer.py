"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal

This is to interface between Wamp client and
container API. 
"""
from docker import Client
from io import BytesIO
from requests.exceptions import HTTPError
import json
import os
import sys
import signal
import tarfile
import time
import StringIO

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
        self._requirement_sh = 'requirement.sh'
        self._fileName = None
        self._filePath = None
        self._folderName = None
        self._extension = None

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

    def transferFile(self, **kwargs):
        """
        Transfers a file to container.

        """

        print ('Transfer routine')
        self._containerName = kwargs['container_name']
        self._containerPath = kwargs['containerpath']
        self._localPath = kwargs['local_path']

        print ('containerName: ,containerPath: ,localPath: ', self._containerName, self._containerPath, self._localPath)
        try:
            _fileObj = open(self._localPath)
        except OSError as err:
            print err.errno == errno.EPERM

        self._fileType = os.path.basename(self._localPath)
        print ('filetype: ', self._fileType)

        _pw_tarstream = BytesIO()
        _pw_tar = tarfile.TarFile(fileobj=_pw_tarstream, mode='w')
        _tarinfo = tarfile.TarInfo(name=self._fileType)
        _tarinfo.size = os.path.getsize(self._localPath)
        _tarinfo.mtime = time.time()
        _pw_tar.addfile(_tarinfo, _fileObj)
        _pw_tar.close()
        _pw_tarstream.seek(0)

        _putArchive_response = invoke_cli.put_archive(self._containerName, self._containerPath, _pw_tarstream)
        print ('_putArchive_response: ', _putArchive_response)

        return _putArchive_response

    def copyFileTo_container(self, **kwargs):
        """
        Copies a file to container.
        """
        print kwargs
        print ('copyFile routine')
        self._containerName = kwargs['container']
        self._containerPath = '/home/'
        self._localPath = kwargs['local_path']

	print ('containerName: ,containerPath: ,localPath: ', self._containerName, self._containerPath, self._localPath)
        (self._filePath, self._fileName) = os.path.split(self._localPath)
        print ('fileName: ,filePath', self._fileName, self._filePath)
        (self._folderName, self._extension) = os.path.splitext(self._fileName)
        print ('folderName: extension: ', self._folderName, self._extension)

        _transferApp = {'container_name': self._containerName, \
                        'containerpath': self._containerPath,  \
                        'local_path': self._localPath}

        _successful = self.transferFile(**_transferApp)
        print ('_successful: ',_successful)

        if _successful:
            self._localPath = os.path.join(self._shellPath, 'untar.sh')
            print self._localPath

            _transferScript = {'container_name': self._containerName, \
                               'containerpath': self._containerPath,  \
                               'local_path': self._localPath}

            _checkStatus = self.transferFile(**_transferScript)

            if _checkStatus:
                _execFile = self._fileType
                print ('executableFile: ', _execFile)
                _fileLocation_inContainer = os.path.join("/home/", _execFile)
                print ('_fileLocation_inContainer: ', _fileLocation_inContainer)

                _executeScript = {'container_name': self._containerName, \
                                  'user': self._user,                    \
                                  '_execFile': _execFile,                \
                                  '_filePath_inContainer': _fileLocation_inContainer
                                  }

                print ('containerName: ,containerPath: ,localPath: execFile: ,filePath_inContainer: ',
                       self._containerName, \
                       self._containerPath, \
                       self._localPath,     \
                       _execFile,           \
                       _fileLocation_inContainer)

                self.run_shellScript(**_executeScript)

                _execFile = self._requirement_sh
                print ('executable_shellFile: ', _execFile)
                _fileLocation_inContainer = os.path.join("/home/", self._folderName, _execFile)
                print ('_fileLocation_inContainer: ', _fileLocation_inContainer)

                _executeScript = {'container_name': self._containerName, \
                                  'user': self._user,                    \
                                  '_execFile': _execFile,                \
                                  '_filePath_inContainer': _fileLocation_inContainer
                                  }
                self.run_shellScript(**_executeScript)

        return _checkStatus
        #os.kill(0, signal.SIGKILL)

    def run_shellScript(self, **kwargs):
        """
        Executes the transferred file.
        """
        print('run_shell routine')
        self._containerName = kwargs['container_name']
        self._user = kwargs['user']
        _execFile = kwargs['_execFile']
        _fileLocation_inContainer = kwargs['_filePath_inContainer']

        self._command = ['sh', _fileLocation_inContainer]
        print ('containerID_shellroutine: ,user: ', self._containerName, self._user)

        _execCreate_response = invoke_cli.exec_create(container=self._containerName, \
                                                      cmd=self._command,             \
                                                      user=self._user)
        print ('_execCreate_response: ', _execCreate_response)

        _execStart_response = invoke_cli.exec_start(exec_id=_execCreate_response)
        print ('_execStart_response: ', _execStart_response)

    def fetch_result(self, **kwargs):
        """
        Fetch a file from a container.
        """
        self._containerName = kwargs['container_name']
        self._retrievePath = kwargs['path_to_retrieveFile']

        (_fetchResult_rawData, _fetchResult_stat) = invoke_cli.get_archive(self._containerName, self._retrievePath)
        print ('stat: ', _fetchResult_stat)

    def fetch_logs(self, **kwargs):
        """
        Fetch logs of a container
        """
        self._containerName = kwargs['container_name']

        _logs = invoke_cli.logs(self._containerName, stream=True)
        for line in _logs:
            print(line)
            
    def fetch_results_using_cp(self,**kwargs):
    	self.containerName = kwargs['container_name']
    	self.resource = kwargs['container_path']
    	
    	print ('container_name:  , container_path:', self.containerName,self.resource)
    	
    	invoke_clientAPI = Client(base_url='unix://var/run/docker.sock', version='1.12')
    	try:
    		print ('try')
    		_fileObtained = invoke_clientAPI.copy(self.containerName,self.resource)
    		filelike = StringIO.StringIO(_fileObtained.read())
		tar = tarfile.open(fileobj = filelike)
		file1 = tar.extractfile(os.path.basename(self.resource))
		x = file1.read()
		
		filename = os.path.join(self._folderName) 
		
		print ('filename: ',filename)
		with open(self._folderName, "w") as text_file:
    			text_file.write(x)

		print ('response: ',_fileObtained)
	except HTTPError:
		print ('exception')

if __name__ == "__main__":
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print dir_path

	#ppid = os.getpid()
	#pid = os.fork()
	#if pid == 0:
    	obj = addFile()
    	
        data = {'container': 'nostalgic_bhabha', \
        	'containerpath': '/home/',       \
        	'local_path': '/home/parallels/Downloads/for_testing.tar'}
	obj.copyFileTo_container(**data)
	
	copyData = {'container_name':'nostalgic_bhabha', \
		    'container_path':'/home/for_testing/requirement.sh'}
		    
	obj.fetch_results_using_cp(**copyData)
	
	"""
	if os.getpid() == ppid :
		print ("parent")
		print ("child PID: ",pid)
		print ("parent PPID: ",ppid)
		while True:
			time.sleep(5)

	"""
# result = {'container_name':'nostalgic_bhabha','path_to_retrieveFile':'/home'}
# obj.fetch_result(**result)

# log = {'container_name':'nostalgic_bhabha'}
# obj.fetch_logs(**log)
