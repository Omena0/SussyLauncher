cls

echo ###### Running automated build ######
cd ../../..
start build.cmd
timeout /t 40
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "C:\Users\aarne\AppData\Roaming\SussyLauncher\"
xcopy "..\..\build\*" "C:\Users\aarne\AppData\Roaming\SussyLauncher\" /E /I /F /Y
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
