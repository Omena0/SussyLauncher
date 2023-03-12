import minecraft_launcher_lib as mcl
import tkinter as tk
import customtkinter as tki
from libraries.sandals import askString, showInfo

print('Select minecraft version:')
version = input('> ')

mc_dir = 'files/'

fabric_version = mcl.fabric.get_latest_loader_version()


def setStatus(text):
    global status
    status = text


def setProgress(text):
    global progress
    progress = text
    print(f'[INSTALLING] Progress: {progress} / {max} [{status}]')


def setMax(text):
    global max
    max = text


callback = {
    "setStatus": lambda text: setStatus(text),
    "setProgress": lambda progress: setProgress(progress),
    "setMax": lambda max: setMax(max)
}

mcl.fabric.install_fabric(version, mc_dir, fabric_version, callback)

showInfo('Fabric succesfully installed!',f'Fabric {version} succesfully installed.')
