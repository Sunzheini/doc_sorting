# -*- coding: utf-8 -*-
import os

from core.database_controller import DatabaseController
from core.engine import Engine
from gui.gui_controller import MyGui


# default_paths (can be changed via the menu) ------------------------------------------------
default_path_for_ready_after_project_name = os.path.join('05 DESIGN DOCUMENTS', 'Работна', 'Ready')
default_path_for_finished_after_project_name = os.path.join('05 DESIGN DOCUMENTS', '020 CLASSIFICATION DRAWINGS')
default_path_for_excel_after_project_name = os.path.join('05 DESIGN DOCUMENTS', '020 CLASSIFICATION DRAWINGS')

# database variables -------------------------------------------------------------------------
database_name = "zed.db"
paths_table_name = "zed_paths_table"
previous_state_table_name = "zed_previous_state_table"

# other variables ----------------------------------------------------------------------------
location_of_log_file = "log.txt"
pdf_scanning_coordinates = {
    'project_name': {'x1': 2135, 'y1': 1527, 'x2': 2355, 'y2': 1556},
    'project_description': {'x1': 2135, 'y1': 1565, 'x2': 2355, 'y2': 1598},
    'document_number': {'x1': 2135, 'y1': 1608, 'x2': 2310, 'y2': 1640},
}

# general info -------------------------------------------------------------------------------
# compile to exe: pyinstaller --onefile --noconsole main.py
# regular expression folders: https://regex101.com/r/Lo8BEL/1
# regular expression files: https://regex101.com/r/f9ipcV/1

if __name__ == '__main__':
    # delete the log file in the beginning
    with open(location_of_log_file, 'w', encoding='utf-8') as file:
        file.write('')

    # initialize the database controller, engine and gui with respective parameters
    db_controller = DatabaseController(
        database_name,
        paths_table_name,
        previous_state_table_name,
    )
    engine = Engine(
        location_of_log_file,
        pdf_scanning_coordinates,
        db_controller,
        paths_table_name,
        previous_state_table_name,
    )
    gui = MyGui(
        engine,
        db_controller,
        default_path_for_ready_after_project_name,
        default_path_for_finished_after_project_name,
        default_path_for_excel_after_project_name,
        paths_table_name,
        previous_state_table_name,
    )
    gui.run()
