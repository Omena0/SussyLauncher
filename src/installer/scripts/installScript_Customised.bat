cls
echo off
echo ###### Running automated build ######
cd ../../..
start build.cmd /wait /b
rem wait for build to finish
timeout /t 60
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "C:\Users\aarne\AppData\Roaming\.SussyLauncher\"
xcopy "..\..\build\*" "C:\Users\aarne\AppData\Roaming\.SussyLauncher\" /E /I /F /Y
copy "..\..\fabric_install.py" "C:\Users\aarne\AppData\Roaming\.SussyLauncher\"
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
