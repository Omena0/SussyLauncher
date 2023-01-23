cls

echo ###### Running automated build ######
cd ../../..
start build.cmd
timeout /t 40
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "{{installPath}}"
xcopy "..\..\build\*" "{{installPath}}" /E /I /F /Y
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
