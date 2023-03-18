import customtkinter as tki
import os
import sys
import subprocess as s
import pyshortcuts as pys

tkfont = tki.CTkFont
tkframe = tki.CTkFrame
tkbutton = tki.CTkButton
tklabel = tki.CTkLabel
tkscrollbar = tki.CTkScrollbar
tkprogressbar = tki.CTkProgressBar
tkoptionmenu = tki.CTkOptionMenu
tkcanvas = tki.CTkCanvas
tktextbox = tki.CTkTextbox
tkcheckbox = tki.CTkCheckBox

tki.set_appearance_mode('dark')

debug = __debug__

appdata = os.getenv('appdata')
print(f'{appdata=}')

try:
    os.chdir('src/installer')
    print('Dir changed to src/installer')
except:
    print('Could not change dir to src/installer')

# installPath = %appdata%/.SussyLauncher/


def install():
    with open('scripts/installScript.bat', 'r') as file:
        content = file.readlines()

    # Disable buttons
    installPath = input.get('0.0', 'end').replace('%appdata%', appdata)
    input.configure(state='disabled')
    checkbox.configure(state='disabled')
    installButton.configure(state='disabled')

    # Generate script depending on {installPath}
    newContent = []
    for i in content:
        cmd = i.replace('{{installPath}}', installPath.replace('\n', ''))
        newContent.append(cmd)
    with open('scripts/installScript_Customised.bat', 'w') as file:
        file.writelines(newContent)

    # Install

    # Shortcut
    os.system(f'mkdir {installPath}')
    a = installPath.replace("\n", "")
    with open(f'{a}run.cmd', 'w') as file:
        file.write('')
    with open(f'{a}run.cmd', 'a') as file:
        file.write(f'cd {installPath}\n')
        file.write(
            'start "" "SussyLauncher/SussyLauncher V1.6/SussyLauncher V1.6.exe"')

    os.system(
        f'mkdir "{a}SussyLauncher\\SussyLauncher V1.6\\minecraft_launcher_lib"')
    open(f'{a}SussyLauncher\\SussyLauncher V1.6\\minecraft_launcher_lib\\version.txt', 'w').close()

    pys.make_shortcut(script=f'{a}run.cmd', name='Sussy Launcher V1.6',
                      desktop=True, startmenu=True, terminal=False)

    # Rest of the files
    os.chdir('scripts')
    os.startfile('installScript_Customised.bat')


def custom_path():
    if checkbox_state.get() == 'on':
        input.configure(state='normal')
    else:
        input.delete('0.0', 'end')
        input.insert('0.0', '%appdata%\.SussyLauncher')
        input.configure(state='disabled')


class App(tki.CTk):
    def __init__(self, title):
        super().__init__()
        self.geometry(f"{500}x{400}")
        self.title(title)
        if not debug:
            self.resizable(False, False)


app = App('SussyLauncher V1.6 Installer')

main = tkframe(master=app, width=1000, height=1000, corner_radius=15)
main.pack(padx=10, pady=10, ipady=30, ipadx=30)

titleText = 'SussyLauncher V1.6 installer'
text = '\nInstallation path:'

title = tklabel(master=main, text=titleText, font=tkfont(
    size=25), anchor='center', height=50, width=100)
title.grid(row=0, column=0)

text = tklabel(master=main, text=text, font=tkfont(size=20),
               anchor='center', height=50, width=500, wraplength=500)
text.grid(row=1, column=0)

input = tktextbox(master=main, corner_radius=10, width=350,
                  height=25, activate_scrollbars=False)
input.grid(row=2, column=0)

input.insert('0.0', '%appdata%\\.SussyLauncher\\')
input.configure(state='disabled')

checkbox_state = tki.StringVar(master=main, value='off')

checkbox = tkcheckbox(master=main, width=50, height=50, text='Custom path',
                      command=custom_path, variable=checkbox_state, onvalue='on', offvalue='off')
checkbox.grid(row=3, column=0)


installButton = tkbutton(master=main, text='Install',
                         font=tkfont(size=30), command=install)
installButton.grid(row=4, column=0)

filler = tklabel(master=main, width=1000, height=1000,
                 text='Ur not supposed to see this', anchor='center')
filler.grid(row=99, column=99)


app.mainloop()
