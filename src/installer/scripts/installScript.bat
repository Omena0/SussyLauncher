cls
echo off
echo ###### Running automated build ######
cd ../../..
start build.cmd /wait /b
rem wait for build to finish
timeout /t 120
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "{{installPath}}"
xcopy "..\..\build\*" "{{installPath}}" /E /I /F /Y
copy "..\..\fabric_install.py" "{{installPath}}"
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
