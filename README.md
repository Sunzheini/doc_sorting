# Doc Sorter

## Purpose
This an application in python to extract info, move, archive and delete folders / documents.
This is done for a specific use case, but can be modified to suit other use cases.
The app uses tkinter for the GUI and pytesseract for OCR.


## To run the app do the following: (or see the instruction in the `information` folder in bulgarian)
1. Install python
2. You need to install pytesseract using Windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki.
3. Note the folder where pytesseract is installed and add it into the system variable 'Path'.
4. Install the python packages using the command: `pip install -r requirements.txt`
5. The program needs a specific folder structure to work. This will be described in the future. Otherwise,
you can modify the code to suit your needs / folder structure.
6. See the video for a use case in the `information` folder.
7. Run the exe or the python project. The exe is compiled with pyinstaller.
8. To compile to exe: `pyinstaller --onefile --noconsole main.py`
9. regular expression folders: https://regex101.com/r/Lo8BEL/1
10. regular expression files: https://regex101.com/r/f9ipcV/1


## App structure
1. main.py - the main file to run the app
2. gui package - contains the gui files, including:
    - gui_controller.py: the controller for the gui
    - default_status_text.py: the default status text status label on the gui
    - front_end_settings.py: the settings for the gui
3. core package - contains the core files, including:
    - database_controller.py: the controller for the database
    - engine.py: the engine of the app. Provides the actual sequence of actions when pressing 
the buttons, which is:
       1) scan the ready directory
       2) scan the Excel file
       3) create the boilerplate folders acc. to the Excel file in the finished directory
       4) scan the finished directory
       5) compare the ready and finished directories
       6) ???
       7) Move files from ready to finished
    - module_controller.py: ???
4. support folder:
    - constants.py: contains the constants for the app
    - decorators.py: contains the decorators for the app, including the timer decorator
    - formatting.py: contains the formatting functions for strings
    - 
5. information folder:
    - contains information in bulgarian how to make the app work
    - contains a video of the app in action
6. dotnet folder:
    - contains a .Net Framework 4.8 Class Library project, which provides useful methods
for folder and file manipulation.
7. dll_controller folder:
    - ???
