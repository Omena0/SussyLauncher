cls
echo off
echo ###### Running automated build ######
cd ../../..
start "" /b /w cmd /c build.cmd
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "{{installPath}}"
xcopy "..\..\build\" "{{installPath}}" /E /I /F /Y
xcopy "..\..\fabric_install.py" "{{installPath}}" /E /I /F /Y
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
