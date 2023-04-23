echo off
cls

echo .
echo ###############################
echo #  BUILD SCRIPT BY OMENA0MC   #
echo ###############################
echo .

cd ../../..


echo .
echo #######################
echo #  RUNNING AUTOMATED  #
echo #        BUILD        #
echo #######################
echo .

echo .
echo #####################
echo #     BUILDING      #
echo #####################
echo .

pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "{{site_packages_path}}\customtkinter;customtkinter"  "src/SussyLauncher V1.7.pyw"
pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "%appdata%\Python\Python311\site-packages\customtkinter;customtkinter" "src/SussyLauncher V1.7.pyw"

echo .
echo #####################
echo #     COPYING       #
echo #####################
echo .

echo .
echo ## Copying assets ##
echo .

xcopy "src/assets/*" "src/build/assets" /E /I /F /Y

echo .
echo ## Copying data ##
echo .

xcopy "src/data/*" "src/build/data" /E /I /F /Y

echo .
echo ## Copying libraries ##
echo .

xcopy "src/libraries/*" "src/build/libraries" /E /I /F /Y

echo .
echo #####################
echo #     BUILD DONE    #
echo #####################
echo .

echo .
echo #####################
echo #    INSTALLING     #
echo #####################
echo .

mkdir "{{install_path}}"
xcopy "src\build\" "{{install_path}}" /E /I /F /Y
xcopy "src\fabric_install.py" "{{install_path}}" /E /I /F /Y

py -c "import tkinter.messagebox;tkinter.messagebox.showinfo('Install complete!', 'SussyLauncher has been installed!')"
