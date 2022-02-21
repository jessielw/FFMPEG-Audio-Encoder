# FFMPEG Audio Encoder # 

## Supported Operating Systems ##
Windows 7 **(x64)**, Windows 8 **(x64)**, Windows 10 **(x64)**, and Windows 11 **(x64)**

# How to use #
## Main Gui ##
1. Extract program from archive to a folder of your choice
2. Select **Open File** or **drag and drop** a single file into the 'Open File' button or the entry box directly to the right
   - You can open any video file, mkv/mp4/etc... or any audio file this way
   - *If there is a file type that is not supported that should be supported please create an **issue** here on the tracker*
   - https://github.com/jlw4049/FFMPEG-Audio-Encoder/issues
3. Once a source file is loaded into the program, the option **to select codec** becomes available
   - You can select what ever codec you want in the list to encode with
   - Once selected **Audio Settings** becomes available
4. Each codec will open a different **Audio Settings** window, but they all function pretty much the same
   - Which contains **Track Tools** menu in the top left hand corner
   - Here you can either view the track information via a custom GUI window or play the selected file with the included MPV player
   - *What ever track is selected in the main window before you open a file with MPV player, the player will automatically play that track if it's a multi-track file*
   - After you select the settings you'd like to encode with. You can either select **View Command** or **Apply**
   - **View Command** will show the command that will be sent to FFMPEG/QAAC/fdk-aac/etc to encode with
   - **Apply** locks in the settings and closes the **Audio Settings** window for that codec
5. **Save File** and **Start Job** becomes available
   - The GUI automatically selects a file save location as well as a name based off of the file input, if you'd like to change either of these select **Save File**
   - **Start Job** will start the encode via the command/settings you chose. You have a chance to select **Show Command** if you want to double check any settings before you start the encode
6. **In the event of an error**
   - On the top of the GUI select **Options -> Shell Options -> Debug** 
   - Try the encode with the same settings, to see where the error lies. You can copy and paste the error from the cmd window. If it's an issue with program post on the Issue tracker or on the Doom9 forum.
7. **Batch Process** is the final button the main GUI
   - The settings work pretty much the same, you drop a couple GUI features like Track Information, MPV player etc.
   - You can either open a directory or drag and drop a directory into the **Open Directory button or text box to the right**
   - **Common Extensions** can be fine tuned for individual files, if you have a mix up in a single folder, however this setting will work for most people
   - Other than that, the rest of the batch gui works pretty much the same as above
 8. **Simple-Youtube-DL-GUI** is merged with this program, it's a custom GUI to download videos/audio from popular websites like youtube etc, this program is paired with this GUI, but if you need support please follow this link https://github.com/jlw4049/Simple-Youtube-DL-GUI to post any issues or feedback
   - You can access it via the **Tools** menu in the GUI or by downloading the standalone version from https://github.com/jlw4049/Simple-Youtube-DL-GUI/releases

## Guide to building the program yourself: (Windows)
1.) **List of required files**
- Latest version of Python (Python 3.8.8 (or under to maintain windows 7/8 support))
- Something to build the program, I use Pyinstaller
  - Open CMD Prompt and use run command `pip install PyInstaller` to install Pyinstaller
- You'll need to manually add TkinterDND for the program to function correctly (Tkinter does not natively support drag and drop)
  - You'll need two files https://github.com/petasis/tkdnd/releases (tkdnd-X.X.X-windows-x86.zip)
) and https://sourceforge.net/projects/tkinterdnd/files/latest/download
  - You need to place `tkdnd2.9.2` folder in **BOTH** `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\tcl` and `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\tcl\tcl8.6` directories
  - For the second file you downloaded you'll want to place the folder `TkinterDnD2` in directory `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\Lib\site-packages`

2.) **With all the required files/programs installed correctly you can use your favorite terminal to build the program**
  - Navigate to `FFMPEG Audio Encoder` folder in what ever terminal/console you are using
  - Your directory should look like this
  https://i.imgur.com/UYXCi0E.png
  - You'll then run the command `pyinstaller -w --onefile --icon="D:\Python Stuff\FFMPEG Audio Encoder\Runtime\Images\icon.ico" FFMPEGAudioEncoder.py`
  - You'll get several new files in the directory, you are only interested in the `Dist` folder, which is where your compressed .exe file will be
  - Move the new `FFMPEGAudioEncoder.exe` file into a seperate folder, copy the `Apps` and `Runtime` folder into the folder where you moved `FFMPEG...exe` and the program will run. 
  - If you have done everything correctly your folder structure will look like this https://i.imgur.com/29ePmxV.png
