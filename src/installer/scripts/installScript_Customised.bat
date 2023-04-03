cls
echo off
echo ###### Running automated build ######
cd ../../..
start "" /b /w cmd /c build.cmd
cd src/installer/scripts

echo ###### Moving files to installPath ######
mkdir "C:\Users\aarne\AppData\Roaming\.SussyLauncher\"
xcopy "..\..\build\" "C:\Users\aarne\AppData\Roaming\.SussyLauncher\" /E /I /F /Y
xcopy "..\..\fabric_install.py" "C:\Users\aarne\AppData\Roaming\.SussyLauncher\" /E /I /F /Y
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
