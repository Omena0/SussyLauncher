import sys
import subprocess
import webbrowser as w
import minecraft_launcher_lib as mcl
import tkinter as tk
import customtkinter as tki
import json
import os
from threading import Thread
import socket
import datetime as t
from tkinter import messagebox
showInfo = messagebox.showinfo

# Rick roll on april first :)
if (t.date.day, t.date.month) == (4,1):
    print('April 1st (get rickrolled lmao)')
    w.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ',2,True)

version = 'V1.7'

print(f'SussyLauncher {version} build 18')

tkfont = tki.CTkFont
tkframe = tki.CTkFrame
tkbutton = tki.CTkButton
tklabel = tki.CTkLabel
tkscrollbar = tki.CTkScrollbar
tkProgressbar = tki.CTkProgressBar
tkOptionMenu = tki.CTkOptionMenu
tkCanvas = tki.CTkCanvas

s = socket.socket()

### SET ALL THE VALUES BELLOW TO FALSE BEFORE BUILDING! ###

# Allows the window to be resized. might add more to this value.
debug = False

# Set this to true to not have to log in, good for UI testing.
# DISCLAIMER: YOU CANT RUN MC WITHOUT SIGNING IN!!!
# This isint a pirate launcher!!!
logged_in = False

###########################################################

optionsText = """#OPTIONS.py:
# YOU CAN EDIT VALUES HERE!

#Use the blurred version of the login background image [1 = True, 0 = False]
blur_background:
1

# Makes the news text font bigger or smaller
font_size_multiplier:
1.5

# Use files/versions/<version>/saveData for minecraft data instead of files/saveData for FABRIC ONLY [1 = True, 0 = False]
fabric_saveData:
1

# Name says it all [1 = True, 0 = False]
leave_launcher_open:
0

# Whitelist you on Omena0MC's servers automatically when launching, BUT YOU NEED TO ASK OMENA TO GIVE U AN ACCOUNT!! [1 = True, 0 = False]
whitelist:
1

# Whitelist username (same as minecraft)
username:
Example_1234

# Whitelist password (dont worry it is hashed immidiately)
password:
Example_Password_1234


### THEESE VALUES YOU SHOULD NOT CHANGE EVER!!! ###

# Ip for whitelist server
whitelist_ip:
127.0.0.1



"""


try:
    with open('data/options.txt') as config:
        config = config.read().split('\n')
        
        blur_background     =  int(config[5])
        textSizeMultiplier  =  float(config[9])
        fabric_saveData     =  int(config[13])
        leave_launcher_open =  int(config[17])
        whitelist           =  int(config[21])
        whitelist_username  =  str(config[25])
        whitelist_password  =  str(config[29])
        whitelist_ip_addr   =  '127.0.0.1'
        whitelist_port      =  5000
        
        
except (FileNotFoundError,IndexError):
    with open('data/options.txt', 'w') as file:
        file.write(optionsText) # Create and add default settings
        
        # Set default values
        blur_background     = 1
        textSizeMultiplier  = 1.5
        fabric_saveData     = 1
        leave_launcher_open = 0
        whitelist           = 0
        whitelist_username  = ''
        whitelist_password  = ''
        whitelist_ip_addr   = '127.0.0.1'
        whitelist_port      = 5000
        


defaultNewsText = 'Build 18: Small adjustments.\nDynamic font size and more!                     '
defaultNewsText += ' '*round(len(defaultNewsText)/textSizeMultiplier)


minecraft_directory = 'files/'
gamedir = 'files/saveData'
installed_versions = mcl.utils.get_installed_versions('files/')
installed_version_ids = []
all_versions = mcl.utils.get_available_versions('files/')
for i in installed_versions:
    print(f'Version found: {i["id"]}')
    installed_version_ids.append(i['id'])

CLIENT_ID = '347cf8bd-c8d1-4967-8104-ee7493cfbf2f'
REDIRECT_URL = 'http://localhost/returnUrl'
SECRET = 'E2V8Q~Y-QIJBxfo4td2E5fTShej0XSeAPZgzGbMA'

# Functions

def get_font_size(text):
    size = 50
    while round(size*len(text)) > 1500:
        size = size - 1
    return size


def install():
    callback = {
        "setStatus": lambda text: progressBar.setStatus(text),
        "setProgress": lambda progress: progressBar.setProgress(progress),
        "setMax": lambda max: progressBar.setMax(max)
    }
    launchProgress.start()
    mcl.install.install_minecraft_version(launchSelector.get(
    ), minecraft_directory=minecraft_directory, callback=callback)
    print('Install complete!')
    showInfo('Done!', 'Install complete!\nPlease restart the launcher!!!')
    newsLabel.configure(text=defaultNewsText)
    launchProgress.stop()


def whitelist():
    print('Attempting to whitelist...')
    try: s.connect((whitelist_ip_addr,whitelist_port))
    except: print('Could not connect! Is the server online???')
    
    s.send(f'GET TOKEN|{whitelist_username}|{whitelist_password}'.encode())
    token = s.recv(2048).decode()
    print(token)
    if token.startswith('TOKEN'):
        s.send(f'REQUEST WHITELIST|{token}'.encode())
        a = s.recv(2048).decode()
        print(a)
    else:
        #showInfo('Invalid Credentials','Invalid Whitelist Credentials..')
        print('Invalid credentials')
    
    

def launch():
    global currentPage
    if not logged_in:
        showInfo('You arent logged in!','Log in with a microsoft account to continue.')
        return
    if currentPage == 'Install':
        if launchSelector.get() in installed_versions:
            showInfo('Version already installed!',f'The version {launchSelector.get()} is a lready installed in "files/versions"! Install cancelled!')
        print(f'[LAUNCHER] Installing {launchSelector.get()}!')
        Thread(target=install, daemon=True, name='Installer').start()
        print(f'[LAUNCHER] Installed {launchSelector.get()}! RESTART')
        return
    
    if currentPage == 'Join':
        join = True
    else:
        join = False
    
    print(f'[LAUNCHER] Launching {currentPage}')

    if pages == ['Install','Join']:
        showInfo('Minecraft missing!', 'You need to install a version first!')
        return

    global login_data
    # Get Minecraft command
    
    if 'fabric' in currentPage and fabric_saveData:
        print('fabric version detected!!!')
        gameDirectory = f'files/versions/{currentPage}/saveData'
    else:
        print('Non-fabric version detected!!!')
        gameDirectory = gamedir
    
    port = '25565'
    
    options = {
        "username": login_data["name"],
        "uuid": login_data["id"],
        "token": login_data["access_token"],
        "jvmArguments": ['-Xmx4G', '-XX:+UnlockExperimentalVMOptions', '-XX:+UseG1GC', '-XX:G1NewSizePercent=20', '-XX:G1ReservePercent=20', '-XX:MaxGCPauseMillis=50', '-XX:G1HeapRegionSize=32M'],
        "gameDirectory": gameDirectory,
        "launcherName": "SussyLauncher", # The name of your launcher
        "launcherVersion": version # The version of your launcher
    }
    
    if join:
        currentPage = launchSelector.get()
        options["server"] = ip.get()
        options["port"] = port

    global minecraft_command
    minecraft_command = mcl.command.get_minecraft_command(currentPage, minecraft_directory, options)

    # Get whitelisted :)
    Thread(target=whitelist,daemon=True).start()
    
    # Start Minecraft
    Thread(target=_launch_mc, daemon=True, name='Minecraft').start()
    if leave_launcher_open == 0: app.destroy()


def _launch_mc():
    global minecraft_command
    subprocess.call(minecraft_command)


def openPage(page):
    print(page)
    global currentPage
    currentPage = page
    
    with open('data/currentPage.txt', 'w') as file:
        file.write(page)
    
    if page == 'Install':
        launchButton.configure(text='Install')
        newsLabel.configure(text=defaultNewsText,height=250,font=newsFont)
        launchSelector.grid_configure(row=0, column=0)
        launchSelector.configure(values=versions)
        ipEntry.place_configure(x=999, y=999)
        
    elif page == 'Join':
        launchButton.configure(text='Join')
        text = 'Automatically join server with mc version:'
        newsLabel.configure(text=text,height=210,font=tkfont(size=get_font_size(text)))
        launchSelector.grid_configure(row=1, column=0)
        launchSelector.configure(values=installed_version_ids)
        ipEntry.grid_configure(row=0,column=0)
    
    else:
        launchButton.configure(text='Launch')
        text = f'Ready to launch.\nClick "launch" to launch {page}!'
        newsLabel.configure(text=text, font=tkfont(size=get_font_size(text)),height=288)
        launchSelector.place_configure(x=999, y=999)
        launchSelector.configure(values=versions)
        ipEntry.place_configure(x=999, y=999)


def login(enable_manual=True):
    global login_data, logged_in
    if logged_in:
        loginApp.destroy()
        return
    # Try login from stored login info
    print('[LAUNCHER] Logging in...')
    # Try to refresh login from stored credentials
    try:
        with open('data/credentials.txt', 'r') as file:
            content = file.read()
        old_login_data = json.loads(content)
        print('[LAUNCHER] Refreshing credentials...')
        login_data = mcl.microsoft_account.complete_refresh(
            client_id=CLIENT_ID, client_secret=SECRET, redirect_uri=REDIRECT_URL, refresh_token=old_login_data["refresh_token"])
        print('[LAUNCHER] Logged in! Storing login data...')
        with open('data/credentials.txt', 'w') as file:
            file.write(json.dumps(login_data))
        logged_in = True
        

    # Otherwise ask the user to log in manually and store login info
    except Exception as e:
        if not enable_manual:
            return
        print(e)
        login_url, state, code_verifier = mcl.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URL)
        w.open(login_url, 2, True)
        code_url = tki.CTkInputDialog(title='Enter URL', text='Enter the URL where you were redirected to after signing in.').get_input()
        auth_code = mcl.microsoft_account.get_auth_code_from_url(code_url)
        # Get the login data
        try:
            login_data = mcl.microsoft_account.complete_login(
                CLIENT_ID, SECRET, REDIRECT_URL, auth_code, code_verifier)
        except KeyError as e:
            return
        with open('data/credentials.txt', 'w') as file:
            file.write(json.dumps(login_data))

        logged_in = True
        showInfo('Logged in!', f'Logged in as {login_data["name"]}')

    file.close()
    loginApp.destroy()

# PREP FOR GUI


latest_version = mcl.utils.get_latest_version()["release"]


with open('data/currentPage.txt','r') as file:
    currentPage = file.read()

tki.set_appearance_mode('dark')
tki.set_default_color_theme('blue')

# LOGIN SCREEN

# Try login without opening browser in case the auto login fails.
try:
    login(enable_manual=False)
except: pass

class App(tki.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{600}x{500}")
        if not debug:
            self.resizable(False, False)

if not logged_in:
    


    loginApp = App()
    loginApp.title('Log in to SussyLaucher')

    # Background
    main = tkframe(master=loginApp, width=1000, height=1000)
    main.pack()

    canvas = tkCanvas(master=main, height=600, width=800, highlightthickness=0)
    canvas.pack(expand=True, fill='both')

    if blur_background == 1:
        bgImage = tk.PhotoImage(file='assets/bg_blurred.png')
    else:
        bgImage = tk.PhotoImage(file='assets/bg.png')
    bgImage = bgImage.zoom(4, 6)
    bgImage = bgImage.subsample(10)

    canvas.create_image(0, 0, image=bgImage, anchor='nw')
    canvas.create_text(375, 150, text='Log in to SussyLauncher:',
                       font=tkfont(size=60), fill='white', anchor='center')

    login = tkbutton(master=main, text='Log in', font=tkfont(
        size=25), width=70, height=50, corner_radius=5, bg_color='transparent', command=login)
    login.place(x=270, y=375)

    loginApp.wm_attributes('-transparentcolor', 'grey')

    loginApp.mainloop()

# CHECK LOGIN STATUS
if not logged_in:
    sys.exit()

# INIT MAIN GUI
pages = ['Install','Join']

for i in installed_versions:
    i = i['id']
    pages.append(i)

pageCommands = []

for page in pages:
    exec(
        f'def page_{page.replace(".","_").replace("-","_")}(): openPage("{page}")')
    exec(f'pageCommands.append(page_{page.replace(".","_").replace("-","_")})')


app = App()
app.title(f'SussyLauncher {version}')

newsFontSize = 50
while round(newsFontSize*len(defaultNewsText)/1.3) > 4100:
    newsFontSize = newsFontSize - 2


newsFont = tkfont(size=newsFontSize)


main = tkframe(master=app, width=1000, height=1000,corner_radius=15, fg_color='transparent')
main.pack(padx=10, pady=10)

title = tklabel(master=main, font=tkfont(size=40),text=f'SussyLauncher {version}', width=50, height=10)
title.grid(row=0, column=1, padx=25, pady=0, sticky='n')

sideFrame = tkframe(master=main, width=100, height=200, corner_radius=15)
sideFrame.grid(row=0, column=0, pady=25, padx=5, ipady=10, ipadx=10, rowspan=100, sticky='NSEW')


for i in enumerate(pages):
    index = i[0]
    i = i[1]
    if 'fabric' in i:
        i = i.split('-')[0] + '_' + i.split('-')[3]
    print(f'Initializing page: {i}')
    a = 25-round((len(i)+1)/2)
    button = tkbutton(master=sideFrame, width=40, height=30, corner_radius=7,text=i, font=tkfont(size=a), command=pageCommands[index])
    button.pack(padx=3, pady=10)

contentFrame = tkframe(master=main, width=350, height=250, corner_radius=25)
contentFrame.grid(row=1, column=1, stick='n', pady=10, padx=10)

newsLabel = tklabel(master=contentFrame, width=350, height=200, text=defaultNewsText, font=newsFont, anchor='n', wraplength=340)
newsLabel.pack(padx=20, pady=10)


class progressBar:
    def __init__(self):
        self.status = 'None'
        self.progress = 0
        self.max = 1

    def setStatus(self, status):
        self.status = status

    def setProgress(self, progress):
        self.progress = progress
        print(f'[LAUNCHER] Progress: {progress} / {self.max} [{self.status}]')
        launchProgress.set(progress/self.max)
        text = f'[Installing {launchSelector.get()}] \nProgress: {progress} / {self.max} \n[{self.status}]'+' '*10
        size = 100
        while round(size*len(text)/1.3) > 2050:
            size = size - 2
        newsLabel.configure(text=text, font=tkfont(size=size))

    def setMax(self, max):
        self.max = max


progressBar = progressBar()


versions = ['1.8.9','1.12.2','1.16.1','1.17.1','1.18.2','1.19.3','1.19.4']

launchFrame = tkframe(master=main, corner_radius=20)
launchFrame.grid(row=2, column=1)

launchSelector = tkOptionMenu(master=launchFrame, corner_radius=15, values=versions)
launchSelector.grid(column=0, row=0, pady=5, padx=5)


launchButton = tkbutton(master=launchFrame, width=200, height=75,corner_radius=15, text='Install', font=tkfont(size=20), command=launch)
launchButton.grid(column=0, row=2, pady=5, padx=5)

launchProgress = tkProgressbar(master=launchFrame, corner_radius=15, mode='determinate', determinate_speed=0.001)
launchProgress.set(0)
launchProgress.grid(column=0, row=3, pady=5, padx=5)

# Vars
ip = tki.Variable(master=launchFrame,name='ip',value='mc.hypixel.net')

ipEntry = tki.CTkEntry(master=launchFrame,width=175,height=40,corner_radius=15,placeholder_text='IP ADDRESS',font=tkfont(size=20),textvariable=ip)
ipEntry.grid(column=0, row=0)

openPage(currentPage)

app.lift()
app.attributes('-topmost', True)
app.attributes('-topmost', False)

app.mainloop()