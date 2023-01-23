from minecraft_launcher_lib import fabric
from libraries.sandals import showInfo, showWarning
from sys import exit

showWarning('WARNING','SussyLauncher V1.5 DOES NOT support fabric for some reason, USE UR OWN SCRIPT TO LAUNCH IT!')

raw_all_versions = fabric.get_all_minecraft_versions()
all_versions = []
for i in raw_all_versions:
    if i['stable']:
        all_versions.append(i['version'])


mcDir = 'files'

latest_loader = fabric.get_latest_loader_version()

for i in all_versions:
    print(i,end=' | ')

version = input('\n\nSelect Fabric version: ')

if not fabric.is_minecraft_version_supported(version=version):
    showInfo('Error','Unsupported version!')
    exit()

class Info:
    def __init__(self):
        self.status = 0
        self.progress = 0
        self.max = 0
    
    def setStatus(self,status):
        self.status = status
    
    def setProgress(self,progress):
        self.progress = progress
        print(f'[INSTALLER] Progress: {progress} / {self.max} [{self.status}]')

    def setMax(self,max):
        self.max = max

info = Info()

callback = {
    "setStatus": lambda status: info.setStatus(status),
    "setProgress": lambda progress: info.setProgress(progress),
    "setStatus": lambda max: info.setMax(max)
}

fabric.install_fabric(version,mcDir,latest_loader,callback=callback)

showInfo('Done!','Install complete! SussyLauncher DOES NOT support fabric versions! Launch with your own raw script.')