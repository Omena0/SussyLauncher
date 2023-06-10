max = 13

print(f'[IMPORTER] Initializing modules... ')

i = 1
def a():
    global i, max
    print(f'\r[IMPORTER] Importing modules... ({i}/{max})',end='')
    i += 1

import asyncio
a()
import subprocess
a()
import webbrowser as w
a()
import minecraft_launcher_lib as mcl
a()
import minepi
a()
import tkinter as tk
a()
import customtkinter as tki
a()
import json
a()
from threading import Thread
a()
import socket
a()
import datetime as dt
from datetime import datetime
a()
import time as t
a()
from tkinter import messagebox
a()
showInfo = messagebox.showinfo

tkfont = tki.CTkFont
tkframe = tki.CTkFrame
tkbutton = tki.CTkButton
tklabel = tki.CTkLabel
tkscrollbar = tki.CTkScrollbar
tkProgressbar = tki.CTkProgressBar
tkOptionMenu = tki.CTkOptionMenu
tkCanvas = tki.CTkCanvas
tkImage = tki.CTkImage

print()