echo off
cls
echo ##### BUILD.CMD #####

echo #### Building ####
pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "C:\Program Files\Python311\lib\Site-packages\customtkinter;customtkinter"  "src/SussyLauncher V1.7.py"
pyinstaller --specpath "src/build/spec" --distpath "src/build/SussyLauncher" --workpath "src/build/build" --noconfirm --onedir --windowed --add-data "%appdata%\Python\Python311\site-packages\customtkinter;customtkinter"  "src/SussyLauncher V1.7.py"

echo #### Copying Files ####

echo ## Copying assets ##
xcopy "src/assets/*" "src/build/assets" /E /I /F /Y

echo ## Copying data ##
xcopy "src/data/*" "src/build/data" /E /I /F /Y

echo ## Copying libraries ##
xcopy "src/libraries/*" "src/build/libraries" /E /I /F /Y

echo ##### BUILD DONE #####