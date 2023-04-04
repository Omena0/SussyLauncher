rem echo off
cls

rem # BUILD SCRIPT BY OMENA0MC

cd ../../..

echo ###### Running automated build ######

rem ##### BUILD SCRIPT #######
echo ##### BUILD.CMD #####

echo #### Building ####
pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "{{site_packages_path}}\customtkinter;customtkinter"  "src/SussyLauncher V1.7.pyw"
pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "%appdata%\Python\Python311\site-packages\customtkinter;customtkinter" "src/SussyLauncher V1.7.pyw"

echo #### Copying Files ####

echo ## Copying assets ##
xcopy "src/assets/*" "src/build/assets" /E /I /F /Y

echo ## Copying data ##
xcopy "src/data/*" "src/build/data" /E /I /F /Y

echo ## Copying libraries ##
xcopy "src/libraries/*" "src/build/libraries" /E /I /F /Y

echo ##### BUILD DONE #####


rem # MOVE FILES TO INSTALLPATH

echo ###### Moving files to installPath ######
mkdir "{{install_path}}"
xcopy "src\build\" "{{install_path}}" /E /I /F /Y
xcopy "src\fabric_install.py" "{{install_path}}" /E /I /F /Y
py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
