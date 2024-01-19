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
7. Run the exe or the python project. The exe is compiled with pyinstaller. The Excel file needs
to be closed to avoid permission errors.
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
       1) scan the ready directory and create a dictionary
       2) scan the Excel file and create 2 dictionaries
       3) create the boilerplate folders acc. to the Excel file in the finished directory
       4) scan the finished directory and create a dictionary
       5) compare the ready and finished directories and create a dictionary with the items to be moved
       6) check the Excel file to correct the dictionary with the items waiting to be moved. also scans the pdf files
       7) Move files from ready to finished
    - module_controller.py: contains all the steps used in the engine
    - walk_loops.py: the loops for walking the directories, which is the heart of gathering the info
from the directories and then filling in collections with the info
4. support folder:
    - comparators.py: contains the comparators for the app
    - constants.py: contains the constants for the app
    - decorators.py: contains the decorators for the app, including the timer decorator
    - dll_runner.py: contains a controller class fo using methods from .Net Framework 4.8 Class Library dlls
    - excel_reader.py: contains the tool to read from the Excel file
    - extractors.py: extract info from the names of folders and files
    - folder_and_file_manager.py: contains the functions for folder and file manipulation
    - folder_and_file_manager_dotnet.py: contains the functions for folder and file manipulation from the .Net dll above
    - formatters.py: contains the formatting functions for strings
    - pdf_scanner.py: contains the functions for scanning pdf files
    - txt_file_manager.py: contains the functions for txt file writing
5. information folder:
    - contains information in bulgarian how to make the app work
    - contains a video of the app in action
6. dotnet folder:
    - contains a .Net Framework 4.8 Class Library project, which provides useful methods
for folder and file manipulation.
