import os
import subprocess
import psutil

def cleanUp(basePath=".", djmountFolderName=".upnpDevices"):
	completePath = basePath + '/' + djmountFolderName
	subprocess.call(['umount', completePath])
	for process in psutil.process_iter():
		if (process.name == "djmount"):
			process.kill()
	os.rmdir(completePath)

def runDjMount(mountFolderPath):
	return subprocess.Popen(["djmount", mountFolderPath])

def mountFolder(basePath=".", djmountFolderName=".upnpDevices"):
	baseDirContent = os.listdir(basePath)
	mountFolderPath = basePath + "/" + djmountFolderName
	if (djmountFolderName not in baseDirContent):
		newDir = os.mkdir(mountFolderPath)
	mountFolderContent = os.listdir(mountFolderPath)
	if (mountFolderContent == []):
		djmountProcess = runDjMount(mountFolderPath)
	return mountFolderPath
