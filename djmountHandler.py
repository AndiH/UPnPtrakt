import os
import subprocess
import psutil

def cleanUp(djmountFolderName=".upnpDevices"):
	subprocess.call(['umount', djmountFolderName])
	for process in psutil.process_iter():
		if (process.name == "djmount"):
			process.kill()
	os.rmdir(djmountFolderName)

def runDjMount(mountFolderPath):
	return subprocess.Popen(["djmount", mountFolderPath])

def mountFolder(djmountFolderName=".upnpDevices"):
	if not (os.path.exists(djmountFolderName)):
		newDir = os.mkdir(djmountFolderName)
	mountFolderContent = os.listdir(djmountFolderName)
	if (mountFolderContent == []):
		djmountProcess = runDjMount(djmountFolderName)
	return djmountFolderName
