from time import time
startTime = time()
from importer import *

version = 'V1.8'

_print = print

def print(*args):
    date = datetime.utcnow() - datetime(1970, 1, 1)
    ms = round(date.total_seconds()*1000)%1000
    time = f'{t.strftime(f"%H:%M:%S:{ms}"):<12}'
    _print(f'{time} {"".join(args)}')

print(f'SussyLauncher {version} build 29')

s = socket.socket()

### SET ALL THE VALUES BELLOW TO FALSE BEFORE BUILDING! ###

# Allows the window to be resized. might add more to this value.
debug = False

# Set this to true to not have to log in, good for UI testing.
# DISCLAIMER: YOU CANT RUN MC WITHOUT SIGNING IN!!!
# This isint a pirate launcher!!!
logged_in = False

# Overrides the Thread object with one that doesent start a new thread
# THIS WILL ABSOLUTELY DECIMATE START TIMES!!!!
replace_Thread = False

###########################################################

if replace_Thread:
    class Thread:
        def __init__(self,target,args=[],*_args,**_kwargs):
            self.target= target
            self.args = args
        def start(self):
            self.target(*self.args)

optionsText = """
# Use the blurred version of the login background image
blur_background=True

# Makes the news text font bigger or smaller
textSizeMultiplier=1.5

# Whether to leave the launcher open when launching minecraft
leave_launcher_open=False

# Ammount of ram to allocate (GB)
ram=5

# Whether to use custom title bar. Looks better but has a slight performance impact on launcher open
customTitleBar=True

"""

def load_config(fix=False):
    """
    Loads config from file and maps values to global variables.
    
    If config is invalid:
        Replaces config with default config.
        Tries to load again:
            If the config is invalid again:
                Override values.
                Ignore config file.
    """
    global config, blur_background,textSizeMultiplier,leave_launcher_open,allocated_ram,customTitleBar
    print('[CONFIG] Loading config...')
    try:
        with open('data/options.txt','r') as config:
            _config = config.read().split('\n')
            config = {}
            for i in _config:
                if i.startswith('#'): continue
                if i == '': continue
                key,value = i.split('=')
                config[key] = value
                print(f'[CONFIG] {key} = {value}')
                
                
            blur_background     = True if config['blur_background'] == 'True' else False
            textSizeMultiplier  = float(config['textSizeMultiplier'])
            leave_launcher_open = True if config['leave_launcher_open'] == 'True' else False
            allocated_ram       = int(config['allocated_ram'])
            customTitleBar      = True if config['customTitleBar'] == 'True' else False

    except Exception as e:
        with open('data/options.txt', 'w') as file:
            file.write(optionsText) # Create and add default settings
        if fix:
            print(f'[CONFIG] Error! Using default config... [{e}]')
            blur_background     = True
            textSizeMultiplier  = 1.5
            leave_launcher_open = False
            allocated_ram       = 5
            customTitleBar      = True
        else: load_config(fix=True)
    

print('[LAUNCHER] LOADING CONFIG') 
load_config()



defaultNewsText = 'Build 24 - UI V2:\nNew an improved config system.\nRemoved a bunch of deprecated features.\nSee the full changelog in github.'
defaultNewsText += ' '*round(len(defaultNewsText)/25*textSizeMultiplier)


minecraft_directory = 'files/'
gamedir = 'files/saveData'
installed_versions = mcl.utils.get_installed_versions('files/')
installed_version_ids = []
all_versions = mcl.utils.get_available_versions('files/')
for i in installed_versions:
    print(f'[LAUNCHER] Version found: {i["id"]}')
    installed_version_ids.append(i['id'])

CLIENT_ID = '347cf8bd-c8d1-4967-8104-ee7493cfbf2f'
REDIRECT_URL = 'http://localhost/returnUrl'
SECRET = 'pp18Q~9n25zSSOTX7iCaM.0zGHAVP_efrtSxQaHo'

# Functions
print('[LAUNCHER] Initializing functions')

def get_font_size(text,space=1500):
    size = 50
    while round(size*len(text)) > space:
        size = size - 1
    return size


def install():
    callback = {
        "setStatus": lambda text: progressBar.setStatus(text),
        "setProgress": lambda progress: progressBar.setProgress(progress),
        "setMax": lambda max: progressBar.setMax(max)
    }
    launchProgress.start()
    mcl.fabric.install_fabric(launchSelector.get(),minecraft_directory,fabric_ver,callback)
    print('Install complete!')
    showInfo('Done!', 'Install complete!\nPlease restart the launcher!!!')
    newsLabel.configure(text=defaultNewsText)
    launchProgress.stop()


def launch():
    global currentPage
    if not logged_in:
        showInfo('Not logged in!','Try again later.\n(About a second)')
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
        showInfo('Minecraft missing!', 'You need to install a version first!\nHow did you get this error? Create an issue on github or contact Omena0#3610 on discord')
        return

    global login_data
    # Get Minecraft command
    
    gameDirectory = f'files/versions/{currentPage}/saveData'
    
    options = {
        "username": login_data["name"],
        "uuid": login_data["id"],
        "token": login_data["access_token"],
        "jvmArguments": [f'-Xmx{allocated_ram}G', '-XX:+UnlockExperimentalVMOptions', '-XX:+UseG1GC', '-XX:G1NewSizePercent=20', '-XX:G1ReservePercent=20', '-XX:MaxGCPauseMillis=50', '-XX:G1HeapRegionSize=32M'],
        "gameDirectory": gameDirectory,
        "launcherName": "SussyLauncher",
        "launcherVersion": version
    }
    
    if join:
        currentPage = launchSelector.get()
        options["server"] = ip.get().split(':')[0]
        options["port"] = ip.get().split(':')[1]

    global minecraft_command
    minecraft_command = mcl.command.get_minecraft_command(currentPage, minecraft_directory, options)
    
    # Start Minecraft
    Thread(target=_launch_mc, daemon=True, name='Minecraft').start()
    if leave_launcher_open: app.destroy()


def _launch_mc():
    global minecraft_command
    subprocess.call(minecraft_command)


def openPage(page):
    global currentPage
    currentPage = page
    
    with open('data/currentPage.txt', 'w') as file:
        file.write(page)
    
    if page == 'Install': #>OpenPage
        launchButton.configure(text='Install')
        newsLabel.configure(text=defaultNewsText,height=225+25)
        launchSelector.grid_configure(row=0, column=0)
        launchSelector.configure(values=versions)
        ipEntry.place_configure(x=999, y=999)
        
    elif page == 'Join':
        launchButton.configure(text='Join')
        text = 'Automatically join server with mc version:'
        newsLabel.configure(text=text,height=185,font=tkfont(size=get_font_size(text)))
        text = 'Automatically join server with mc version:'
        newsLabel.configure(text=text,height=210,font=tkfont(size=get_font_size(text,space=1500)))
        launchSelector.grid_configure(row=1, column=0)
        launchSelector.configure(values=installed_version_ids)
        ipEntry.grid_configure(row=0,column=0)
    
    else:
        launchButton.configure(text='Launch')
        text = f'Ready to launch.\nClick "launch" to launch {page}!'
        newsLabel.configure(text=text, font=tkfont(size=get_font_size(text)),height=262+25)
        launchSelector.place_configure(x=999, y=999)
        launchSelector.configure(values=versions)
        ipEntry.place_configure(x=999, y=999)



def _login(auto=False):
    start = t.time()
    global login_data, logged_in, username, skins
    if logged_in:
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
        if auto: return 'Failed'
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
    duration = t.time() - start
    print(f'[PERFORMANCE] Login took {duration} Seconds!')

def login():
    if _login(auto=True) == 'Failed':
        loginApp = App()
        titlebar = CustomTitleBar(loginApp)
        titlebar.title('Log in to SussyLaucher')

        # Background
        main = tkframe(master=loginApp, width=1000, height=1000)
        main.pack()

        canvas = tkCanvas(master=main, height=600, width=800, highlightthickness=0)
        canvas.pack(expand=True, fill='both')

        t.sleep(0.1)
        if blur_background:
            bgImage = tk.PhotoImage(file='assets/bg_blurred.png')
        else:
            bgImage = tk.PhotoImage(file='assets/bg.png')
        bgImage = bgImage.zoom(4, 6)
        bgImage = bgImage.subsample(10)

        canvas.create_image(0, 0, image=bgImage, anchor='nw')
        canvas.create_text(375, 150, text='Log in to SussyLauncher:',font=tkfont(size=60), fill='white', anchor='center')

        login = tkbutton(master=main, text='Log in', font=tkfont(
            size=25), width=70, height=50, corner_radius=5, bg_color='transparent', command=_login)
        login.place(x=270, y=375)

        loginApp.wm_attributes('-transparentcolor', 'grey')

        loginApp.mainloop()


def wait_for_login():
    global login_data, logged_in
    while not logged_in: pass
    try:
        name = login_data["name"]
        a = get_font_size(name,space=170)
        playerName.configure(text=f'Logged in as:\n{name}',font=tkfont(size=a))
    except: pass

# >THREADED LOGIN

Thread(target=login, name='Microsoft Login').start()

# PREP FOR GUI

latest_version = mcl.utils.get_latest_version()["release"]

fabric_ver = mcl.fabric.get_latest_loader_version()

async def async_head_render():
    while not logged_in: pass
    p = minepi.Player(uuid=login_data['id'])
    await p.initialize()

    await p.skin.render_head(display_hair=True,vr=0,hr=0)
    
    p.skin.head.save('data/head.png', format='png')
    print('[MINEPI] Head rendered')
    

def head_render():
    print('[MINEPI] Rendering player head..')
    asyncio.run(async_head_render())

print('[LAUNCHER] Starting player head renderer..')
if not debug: Thread(target=head_render,name='Head renderer').start()

with open('data/currentPage.txt','r') as file:
    currentPage = file.read()

tki.set_appearance_mode('dark')
tki.set_default_color_theme('blue')

print('[LAUNCHER] Initializing classes')
class App(tki.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{600}x{500+25}") # 25 for titebar height
        if not debug:
            self.resizable(False, False)
            
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

print('[LAUNCHER] Preparing to Initialize Main GUI')

# INIT MAIN GUI
pages = ['Install','Join']

for i in installed_versions:
    i = i['id']
    print(f'[LAUNCHER] Found Version {i}')
    if 'fabric' in i:
        pages.append(i)
    else: print(f'[LAUNCHER] Ignoring non-fabric version [{i}]')

pageCommands = []

for page in pages:
    exec(f'def page_{page.replace(".","_").replace("-","_")}(): openPage("{page}")')
    exec(f'pageCommands.append(page_{page.replace(".","_").replace("-","_")})')


progressBar = progressBar()

versions = ['1.8.9','1.12.2','1.16.1','1.18.2','1.19.3','1.19.4','1.20.1']

print('[LAUNCHER] Initializing Main GUI')

app = App()
if customTitleBar:
    titlebar = CustomTitleBar(app)
    titlebar.title(f'SussyLauncher {version}')
else: app.title(f'SussyLauncher {version}')

newsFontSize = get_font_size(defaultNewsText,space=2500)

newsFont = tkfont(size=newsFontSize)

main = tkframe(master=app,corner_radius=15, fg_color='transparent',bg_color='transparent')
main.pack(padx=5, pady=5,ipadx=5,ipady=5)

title = tklabel(master=main, font=tkfont(size=40),text=f'SussyLauncher {version}', width=50, height=10)
title.grid(row=0, column=1, padx=25, pady=0, sticky='n')

sideFrame = tkframe(master=main, width=100, height=100, corner_radius=15)
sideFrame.grid(row=0, column=0, pady=10, padx=5, ipady=10, ipadx=10, rowspan=4, sticky='NSEW')



for i in enumerate(pages):
    index = i[0]
    i = i[1]
    if 'fabric' in i: i = i.split('-')[0] + '_' + i.split('-')[3]
    a = 25
    while round(a*len(i)) > 250:
        a = a - 1
    print(f'[LAUNCHER] Initializing page: {i} [{a}]')
    button = tkbutton(master=sideFrame, width=60, height=20, corner_radius=7,text=i, font=tkfont(size=a), command=pageCommands[index])
    button.pack(padx=3, pady=10)

contentFrame = tkframe(master=main, width=350, height=250, corner_radius=25)
contentFrame.grid(row=1, column=1, stick='n', pady=10, padx=10)

newsLabel = tklabel(master=contentFrame, width=350, height=200, text=defaultNewsText, font=newsFont, anchor='n', wraplength=340)
newsLabel.pack(padx=20, pady=10)

bottomFrame = tkframe(master=main,corner_radius=20,bg_color='transparent',fg_color='transparent')
bottomFrame.grid(row=3, column=1)

launchFrame = tkframe(master=bottomFrame, corner_radius=20)
launchFrame.grid(row=0, column=0,padx=5,pady=3)

launchSelector = tkOptionMenu(master=launchFrame, corner_radius=15, values=versions)
launchSelector.grid(column=0, row=0, pady=5, padx=5)


launchButton = tkbutton(master=launchFrame, width=150, height=75,corner_radius=15, text='Install', font=tkfont(size=20), command=launch)
launchButton.grid(column=0, row=2, pady=5, padx=10)

launchProgress = tkProgressbar(master=launchFrame, width=150,corner_radius=15, mode='determinate', determinate_speed=0.001)
launchProgress.set(0)
launchProgress.grid(column=0, row=3, pady=5, padx=5)


profileFrame = tkframe(master=bottomFrame, corner_radius=20)
profileFrame.grid(row=0, column=1,padx=5)

try:
    img = tk.PhotoImage(file='data/head.png',format='png')
    
    canvas = tkCanvas(master=profileFrame, height=100, width=100, highlightthickness=0,bg='#2b2b2b')
    canvas.create_image(0, 0, image=img, anchor='nw')
    canvas.pack(side='right',padx=10,pady=15)

except: pass

a = get_font_size('Logging in...',space=200)

playerName = tklabel(master=profileFrame, text='Logging in...',font=tkfont(size=a))
playerName.pack(side='right',padx=10,pady=10,expand=True,fill='both')

print('[LAUNCHER] Preparing for mainloop')

# Vars
ip = tki.Variable(master=launchFrame,name='ip',value='mc.hypixel.net')

ipEntry = tki.CTkEntry(master=launchFrame,width=175,height=40,corner_radius=15,placeholder_text='IP ADDRESS',font=tkfont(size=20),textvariable=ip)
ipEntry.grid(column=0, row=0)

openPage(currentPage)

print('[LAUNCHER] Starting mainloop...')

Thread(target=wait_for_login,name='Mainloop').start()

app.lift()
app.attributes('-topmost', True)
app.attributes('-topmost', False)

duration = time() - startTime
print(f'[PERFOMANCE] Launcher started in {duration} Seconds!')

app.mainloop()
