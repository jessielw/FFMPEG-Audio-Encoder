# FFMPEG-Audio-Encoder
###### Work in progress...

## Guide to building the program yourself: (Windows)
1.) **List of required files**
- Latest version of Python
- Something to build the program, I use Pyinstaller
  - Open CMD Prompt and use run command `pip install PyInstaller` to install Pyinstaller
- You'll need to manually add TkinterDND for the program to function correctly (Tkinter does not natively support drag and drop)
  - You'll need two files `https://github.com/petasis/tkdnd/releases` (tkdnd-X.X.X-windows-x86.zip)
) and `https://sourceforge.net/projects/tkinterdnd/files/latest/download`
  - You need to place `tkdnd2.9.2` folder in `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\tcl` and `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\tcl\tcl8.6`
  - For the second file you downloaded you'll want to place the folder `TkinterDnD2` in this directory `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\Lib\site-packages`

2.) **With all the required files/programs installed correctly you can use your favorite terminal to build the program**
  - Navigate to `FFMPEG Audio Encoder` folder in what ever ternimal/console you are using
  - Your directory should look like this
  https://i.imgur.com/UYXCi0E.png
  - You'll then run the command `pyinstaller -w --onefile --icon="D:\Python Stuff\FFMPEG Audio Encoder\Runtime\Images\icon.ico" FFMPEGAudioEncoder.py`
  - You'll get several new files in the directory, you are only interested in the `Dist` folder, which is where your compressed .exe file will be
  - Move the new `FFMPEGAudioEncoder.exe` file into a seperate folder, copy the `Apps` and `Runtime` folder into the folder where you moved `FFMPEG...exe` and the program will run. 
  - If you have done everything correctly your folder structure will look like this https://i.imgur.com/29ePmxV.png
