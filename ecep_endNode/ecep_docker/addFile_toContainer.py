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
        self._user = 'root'
        self._fileType = None
        self._status = {}
        self._command = []

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

    def copyFileTo_container(self, **kwargs):
        """
        Copies a file to container.
        """
        print ('copyFile routine')
        self._containerName = kwargs['container_name']
        self._containerPath = kwargs['containerpath']
        self._localPath = kwargs['local_path']

        try:
            _fileObj = open(self._localPath)
        except OSError as err:
            print err.errno == errno.EPERM

        self._fileType = os.path.basename(self._localPath)
        print ('filetype: %s' % 'self._fileType')
        _pw_tarstream = BytesIO()
        _pw_tar = tarfile.TarFile(fileobj=_pw_tarstream, mode='w')  # class for reading and writing tar archives.
        _tarinfo = tarfile.TarInfo(name=self._fileType)  # create an object
        _tarinfo.size = os.path.getsize(self._localPath)
        _tarinfo.mtime = time.time()
        _pw_tar.addfile(_tarinfo, _fileObj)
        _pw_tar.close()
        _pw_tarstream.seek(0)

        _putArchive_response = invoke_cli.put_archive(self._containerName, self._containerPath, _pw_tarstream)
        print ('_putArchive_response: ', _putArchive_response)

        if _putArchive_response:
            _script = {'container_name': self._containerName, 'user': self._user}
            print ('container_name: ', self._containerName)
            self.run_shellScript(**_script)

        return _putArchive_response

    def run_shellScript(self, **kwargs):
        """
        Executes the transferred file.
        """
        print('run_shell routine')
        self._containerName = kwargs['container_name']
        self._user = kwargs['user']
        _execFile = self._fileType
        print ('executableFile: ', _execFile)
        _fileLocation = os.path.join("/", _execFile)
        print _fileLocation
        self._command = ['sh', _fileLocation]
        print ('containerID_shellroutine: ,user: ', self._containerName, self._user)
        _execCreate_response = invoke_cli.exec_create(container=self._containerName, cmd=self._command, user=self._user)
        print ('_execCreate_response: ', _execCreate_response)
        _execStart_response1 = invoke_cli.exec_start(exec_id=_execCreate_response)
        print ('_execStart_response1: ', _execStart_response1)


if __name__ == "__main__":
    obj = addFile()
    name = {'container_name': 'nostalgic_bhabha'}
    obj.startContainer_toAddFile(**name)
    # time.sleep(10)
    data = {'container_name': 'nostalgic_bhabha', 'containerpath': '/', 'local_path': '/home/parallels/hello.sh',
            'file': 'temp.tar'}
    obj.copyFileTo_container(**data)
    # time.sleep(5)
    # script = {'container_name':'nostalgic_bhabha','user':'root'}
    # obj.run_shellScript(**script)
