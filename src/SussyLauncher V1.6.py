import sys
import subprocess
import webbrowser as w
import minecraft_launcher_lib as mcl
import tkinter as tk
import customtkinter as tki
import json
import os
from threading import Thread
from libraries.sandals import askString, showInfo

print('SussyLauncher V1.6 build 7')

tkfont = tki.CTkFont
tkframe = tki.CTkFrame
tkbutton = tki.CTkButton
tklabel = tki.CTkLabel
tkscrollbar = tki.CTkScrollbar
tkProgressbar = tki.CTkProgressBar
tkOptionMenu = tki.CTkOptionMenu
tkCanvas = tki.CTkCanvas

### SET ALL THE VALUES BELLOW TO FALSE BEFORE BUILDING! ###

# Allows the window to be resized. And some other things maybe.
debug = False

# Set this to true to not have to log in, good for UI testing.
# DISCLAIMER: YOU CANT RUN MC WITHOUT SIGNING IN!!!
# This isint a pirate launcher!!!
logged_in = False

###########################################################

defaultNewsText = 'Patch notes: \nFix some bugs, Installer now always installs.\nNot only when python is located in Program Files.'+' '*100


try:
    with open('data/options.txt') as config:
        config = config.read()
except FileNotFoundError:
    open('data/options.txt', 'w').close()
    with open('data/options.txt') as config:
        config = config.read()

if 'blur_background = True' in config:
    blur_background = True
else:
    blur_background = False

minecraft_directory = 'files/'
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
    showInfo('Done!', 'Install complete!')
    newsLabel.configure(text=defaultNewsText)
    launchProgress.stop()


def launch():
    if not logged_in:
        showInfo('You arent logged in!',
                 'Log in with a microsoft account to continue.')
        return
    if currentPage == 'Home':
        if launchSelector.get() in installed_versions:
            showInfo('Version already installed!',
                     f'The version {launchSelector.get()} is a lready installed in "files/versions"! Install cancelled!')
        print(f'[LAUNCHER] Installing {launchSelector.get()}!')
        Thread(target=install, daemon=True, name='Installer').start()
        print(f'[LAUNCHER] Installed {launchSelector.get()}!')
        return

    print(f'[LAUNCHER] Launching {currentPage}')

    if pages == ['Home']:
        showInfo('Minecraft missing!', 'You need to install a version first!')
        return

    global login_data
    # Get Minecraft command
    options = {
        "username": login_data["name"],
        "uuid": login_data["id"],
        "token": login_data["access_token"],
        "jvmArguments": ['-Xmx4G', '-XX:+UnlockExperimentalVMOptions', '-XX:+UseG1GC', '-XX:G1NewSizePercent=20', '-XX:G1ReservePercent=20', '-XX:MaxGCPauseMillis=50', '-XX:G1HeapRegionSize=32M'],
        "gameDirectory": 'files/saveData',

    }

    global minecraft_command
    minecraft_command = mcl.command.get_minecraft_command(
        currentPage, minecraft_directory, options)

    # Start Minecraft
    Thread(target=_launch_mc, daemon=True, name='Minecraft').start()


def _launch_mc():
    global minecraft_command
    subprocess.call(minecraft_command)


def openPage(page):
    print(page)
    global currentPage
    currentPage = page
    if page == 'Home':
        launchButton.configure(text='Install')
        newsLabel.configure(text=defaultNewsText)
        launchSelector.grid_configure(row=0, column=0)
    else:
        launchButton.configure(text='Launch')
        text = f'Ready to launch.\nClick "launch" to launch {page}!'
        newsLabel.configure(text=text, font=newsFont)
        launchSelector.place_configure(x=999, y=999)


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
        
        # Dont show "Logged in!" msgbox when already has logged in before
        #showInfo('Logged in!', f'Logged in as {login_data["name"]}')

    # Otherwise ask the user to log in manually and store login info
    except Exception as e:
        if not enable_manual:
            return
        print(e)
        login_url, state, code_verifier = mcl.microsoft_account.get_secure_login_data(
            CLIENT_ID, REDIRECT_URL)
        w.open(login_url, 1, True)
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

currentPage = 'Home'

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

    if blur_background:
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
pages = ['Home']

for i in installed_versions:
    i = i['id']
    pages.append(i)

pageCommands = []

for page in pages:
    exec(
        f'def page_{page.replace(".","_").replace("-","_")}(): openPage("{page}")')
    exec(f'pageCommands.append(page_{page.replace(".","_").replace("-","_")})')


app = App()
app.title('SussyLauncher V1.6')

newsFontSize = 50
while round(newsFontSize*len(defaultNewsText)/1.3) > 4100:
    newsFontSize = newsFontSize - 2


newsFont = tkfont(size=newsFontSize)


main = tkframe(master=app, width=1000, height=1000,
               corner_radius=15, fg_color='transparent')
main.pack(padx=5, pady=5)

title = tklabel(master=main, font=tkfont(size=40),
                text='SussyLauncher V1', width=50, height=10)
title.grid(row=0, column=1, padx=50, pady=0, stick='n')

sideFrame = tkframe(master=main, width=100, height=200, corner_radius=15)
sideFrame.grid(row=0, column=0, padx=0, pady=100, rowspan=4, stick='nw')


for i in enumerate(pages):
    index = i[0]
    i = i[1]
    if 'fabric' in i:
        i = i.split('-')[0] + '_' + i.split('-')[3]
    print(i[1])
    button = tkbutton(master=sideFrame, width=50, height=30, corner_radius=5,text=i, font=tkfont(size=20), command=pageCommands[index])
    button.pack(padx=10, pady=10)

contentFrame = tkframe(master=main, width=350, height=250, corner_radius=25)
contentFrame.grid(row=1, column=1, stick='n', pady=10)

newsLabel = tklabel(master=contentFrame, width=350, height=250,
                    text=defaultNewsText, font=newsFont, anchor='n', wraplength=340)
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


versions = []
for i in all_versions:
    if i['type'] in ['snapshot', 'old_alpha', 'old_beta']:
        continue
    versions.append(i['id'])

launchFrame = tkframe(master=main, corner_radius=20)
launchFrame.grid(row=2, column=1)

launchSelector = tkOptionMenu(
    master=launchFrame, corner_radius=15, values=versions)
launchSelector.grid(column=0, row=0, pady=5, padx=5)


launchButton = tkbutton(master=launchFrame, width=200, height=75,
                        corner_radius=15, text='Install', font=tkfont(size=20), command=launch)
launchButton.grid(column=0, row=1, pady=5, padx=5)

launchProgress = tkProgressbar(master=launchFrame, corner_radius=15, mode='determinate', determinate_speed=0.001)
launchProgress.set(0)
launchProgress.grid(column=0, row=2, pady=5, padx=5)


app.mainloop()
