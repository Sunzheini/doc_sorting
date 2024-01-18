# -*- coding: utf-8 -*-
from core.database_controller import DatabaseController
from core.engine import Engine
from gui.gui_controller import MyGui
from support.constants import (ready_dir_path, finished_dir_path, excel_file_path,
                               db_name, paths_table_name, previous_state_table_name,
                               location_of_log_file, pdf_scanning_coordinates)


# default_paths (can be changed via the menu) ------------------------------------------------
default_path_for_ready_after_project_name = ready_dir_path        # where we look for ready documents
default_path_for_finished_after_project_name = finished_dir_path  # where we copy the finished documents
default_path_for_excel_after_project_name = excel_file_path       # this is the list of documents


# database constants -------------------------------------------------------------------------
database_name = db_name                                           # name of the database
paths_table_name = paths_table_name                               # name of the table with above paths
previous_state_table_name = previous_state_table_name             # name of the table with previous paths


# other constants ----------------------------------------------------------------------------
location_of_log_file = location_of_log_file                       # where the log file is located
pdf_scanning_coordinates = pdf_scanning_coordinates               # where to look inside the pdf file for info


# start --------------------------------------------------------------------------------------
if __name__ == '__main__':
    # 1. recreate the log file in the beginning
    with open(location_of_log_file, 'w', encoding='utf-8') as file:
        file.write('')

    # 2. initialize the database controller, engine and gui with respective parameters
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

    # 3. run the gui
    gui.run()
