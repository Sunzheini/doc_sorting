# -*- coding: utf-8 -*-
from datetime import datetime
import os
import tkinter as tk
from tkinter import simpledialog

from core.module_controller import ModuleController
from core.project_manager import ProjectManager
from support.constants import location_of_json_file


class Engine:
    """
    This class is the main class of the program. It is responsible for the communication between
    the GUI and the modules. It is also responsible for the initialization of the modules.
    """
    def __init__(
            self,
            location_of_log_file,
            pdf_scanning_coordinates,
            db_controller,
            paths_table_name,
            previous_state_table_name,
    ):
        """
        This function initializes the engine.
        :param location_of_log_file: location of log file
        :param pdf_scanning_coordinates: coordinates for scanning pdf files
        :param db_controller: database controller object
        :param paths_table_name: name of table with paths
        :param previous_state_table_name: name of table with previous paths
        """
        # locations
        self.location_of_log_file = location_of_log_file

        # where to scan the pdf files
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        # database related
        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name

        # Initialize all modules here
        try:
            self.module = ModuleController(location_of_log_file, db_controller, paths_table_name,
                                           previous_state_table_name, pdf_scanning_coordinates)
        except Exception as e:
            print(e)

    def methods_bound_to_button_1(self, project_dir, ready_dir, finished_dir, file_path):
        """
        Execute methods bound to button 1, which is the button for scanning.
        First scan the ready directory, then the Excel file, then the finished directory.
        Then compare the ready and finished directories. Then check if new folders in work
        correspond to Excel file. Then return if ok.
        :param project_dir: Directory of the project.
        :param ready_dir: Directory to scan for ready files.
        :param finished_dir: Directory to move finished files.
        :param file_path: Path to the Excel file.
        :return: Tuple (result message, color, additional_message).
        """
        has_additional_message = False
        additional_message = ""

        # ------------------------------------------------------------------------------
        # Scanners
        # ------------------------------------------------------------------------------
        # 1. Scan ready directory
        result = self.module.step_1_scan_ready_dir(ready_dir)
        if result != 'Success':
            return result, 'red', None

        # 2. Read from Excel file
        result = self.module.step_2_scan_excel(file_path)
        if result != 'Success':
            return result, 'red', None

        # 3. Create folders in finished directory
        result = self.module.step_3_create_folders_in_finished_dir(finished_dir)
        if result != 'Success':
            return result, 'red', None

        # 4. Scan finished directory
        result = self.module.step_4_scan_finished_dir(finished_dir)
        if result != 'Success':
            return result, 'red', None

        # ------------------------------------------------------------------------------
        # Comparators
        # ------------------------------------------------------------------------------
        # 5. Compare ready and finished directories
        result, temp_message = self.module.step_5_compare_ready_to_finished()
        if temp_message is not None:
            has_additional_message = True
            additional_message += '\n' + temp_message
        if result != 'Success':
            return result, 'red', None

        # 6. Check if new folders in work correspond to Excel file
        result, temp_message = self.module.step_6_check_if_new_folders_in_work_and_their_contents_correspond_to_excel_also_fills_destination_paths(finished_dir)
        if temp_message is not None:
            has_additional_message = True
            additional_message += '\n' + temp_message
        if result != 'Success':
            return result, 'red', None

        return ('Сканирането премина успешно', 'green', None) if not has_additional_message \
            else ('Сканирането премина успешно', 'green', additional_message)

    def methods_bound_to_button2(self, source_folder, destination_folder, archive_folder):
        """
        Execute methods bound to button 2. First move files from ready to finished, then
        archive files from finished to archive, then create new folders in finished.
        :param source_folder: Source folder for moving files.
        :param destination_folder: Destination folder for moving files.
        :param archive_folder: Archive folder for archiving files.
        :return: Tuple (result message, color, additional_message).
        """
        has_additional_message = False
        additional_message = ""

        # ----------------------------------------------------------------------------------------
        # Moving
        # ----------------------------------------------------------------------------------------
        # 7. Move files from ready to finished
        result = self.module.step_7_archive_then_new_folders_from_ready_to_finished(source_folder, destination_folder, archive_folder)
        if result != 'Success':
            return result, 'red', None

        return ('Обновяването премина успешно', 'green', None) if not has_additional_message \
            else ('Обновяването премина успешно', 'green', additional_message)

    def methods_bound_to_button4(self, ready_dir):
        """
        Execute methods bound to button 4.
        :return: Tuple (result message, color, additional_message).
        """
        has_additional_message = False
        additional_message = ""

        # ------------------------------------------------------------------------------
        # generating info
        # ------------------------------------------------------------------------------
        try:
            folder_info = []
            for root, dirs, files in os.walk(ready_dir):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    dir_mod_time = datetime.fromtimestamp(os.path.getmtime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
                    folder_info.append(f"Folder: {dir_name} (Last Modified: {dir_mod_time})")

                    # List files within this directory
                    for file_name in os.listdir(dir_path):

                        if file_name.lower() == 'thumbs.db':
                            continue  # Skip Thumbs.db files

                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path):
                            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                                '%Y-%m-%d %H:%M:%S')
                            folder_info.append(f"     File: {file_name} (Last Modified: {file_mod_time})")

                    folder_info.append('')

            if folder_info:
                has_additional_message = True
                additional_message += '\n' + "\n".join(folder_info)
            else:
                additional_message += '\n' + "No folders found."

        except Exception as e:
            return e, 'red', None

        return ('', 'green', None) if not has_additional_message \
            else ('', 'green', additional_message)
