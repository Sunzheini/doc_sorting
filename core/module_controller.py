# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from time import sleep

from support.comparators import compare_by_name_and_number
from support.pdf_scanner import extract_text_from_pdf, split_pdf_scanning_coordinates
from support.excel_reader import read_from_excel_file
from core.walk_loop import the_walk_loop
from support.constants import content_of_excel_file_start_row
from support.folder_and_file_manager import create_directory, directory_exists, archive_directory, delete_directory, \
    move_directory, copy_file
# from support.folder_and_file_manager_dotnet import (create_directory_with_dotnet, delete_directory_with_dotnet,
#                                                     move_directory_with_dotnet, delete_file_with_dotnet,
#                                                     copy_file_with_dotnet)
from support.txt_file_manager import append_a_dict_to_txt_file, append_a_string_to_txt_file
from support.formatters import (normalize_path_to_have_only_forward_slashes)
from support.extractors import extract_text_after_last_backslash


class ModuleController:
    def __init__(
            self,
            location_of_log_file,
            db_controller,
            paths_table_name,
            previous_state_table_name,
            pdf_scanning_coordinates,
    ):
        """
        Initializes the ModuleController object
        :param location_of_log_file: absolute path to the log file
        :param db_controller: the database controller object
        :param paths_table_name: the name of the table in the database where the paths are stored
        :param previous_state_table_name: the name of the table in the database where the previous paths are stored
        :param pdf_scanning_coordinates: the coordinates for scanning the pdf files
        """
        self.location_of_log_file = location_of_log_file

        # database
        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        # structures
        self.dict_contents_of_ready_dir = None          # filled-in by step_1_scan_ready_dir
        self.dict_contents_of_file_by_section = None    # filled-in by step_2_scan_excel
        self.dict_contents_of_file_by_file = None       # filled-in by step_2_scan_excel
        self.dict_contents_of_finished_dir = None       # filled-in by step_4_scan_finished_dir
        self.dict_of_files_to_be_archived = None        # filled-in by step_5_compare_ready_to_finished
        self.dict_waiting_for_execution = None          # filled-in by step_5_compare_ready_to_finished
        # the last one is then corrected by step_6_check_if_new_folders_in_work_and_their_contents_correspond_to_excel

    # ----------------------------------------------------------------------------------------
    # Scanners
    # ----------------------------------------------------------------------------------------
    def step_1_scan_ready_dir(self, ready_dir):
        """
        Scans the ready directory, fills-in a dict and exports the result to a txt file

        example folder: '20230928 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface'


        self.dict_contents_of_ready_dir:
        {'MC077-021-001 Leak proof joint design and drawing for hull': {
            'date': '20230928',
            'rev': 0,
            'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull',
            'files': {
                'MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf': {
                    'number': 'MC077-021-001',
                    'name': 'Leak proof joint design and drawing for hull',
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf'},
                'MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg': {
                    'number': 'MC077-021-001',
                    'name': 'Leak proof joint design and drawing for hull',
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg'}}},

        Note: file_name is None if the actual file name is using the new format, i.e.
        „MC077-022-001_ 30092023-A1.pdf“
        instead of
        „MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf“
        first a search is performed for the old format, then for the new one:
            'files': {
                'MC077-021-001_28092023.dwg': {
                    'number': 'MC077-021-001',
                    'name': None,
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\P\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001_28092023.dwg'},


        :param ready_dir: path to ready dir
        :return: 'Success' or 'Error'
        """
        try:
            self.dict_contents_of_ready_dir = the_walk_loop('ready_dir', ready_dir)
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_ready_dir)
            append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported ready dir to txt file (see above)')
            return 'Success'
        except Exception as e:
            self._log_error_and_return(e)

    def step_2_scan_excel(self, file_path):
        """
        Scans the Excel file, fills-in 2 dicts and exports the result to a txt file

        self.dict_contents_of_file_by_section:
        {'A DRAWINGS': {
            'MC077-022-001 LEAK PROOF JOINT DESIGN AND DRAWING FOR TANK AND DECK SURFACE': {
                'line number': 'A.1',
                'file number': 'MC077-022-001',
                'file name': 'LEAK PROOF JOINT DESIGN AND DRAWING FOR TANK AND DECK SURFACE'},
            'MC077-022-002 PIPE SUPPORT, WALKWAY STRUCTURE EXECUTION DRAWING': {
                'line number': 'A.2',
                'file number': 'MC077-022-002',
                'file name': 'PIPE SUPPORT, WALKWAY STRUCTURE EXECUTION DRAWING'}},}

        self.dict_contents_of_file_by_file:
        {'MC077-022-001 LEAK PROOF JOINT DESIGN AND DRAWING FOR TANK AND DECK SURFACE': {
            'section number': 'A DRAWINGS',
            'line number': 'A.1'},
        'MC077-022-002 PIPE SUPPORT, WALKWAY STRUCTURE EXECUTION DRAWING': {
            'section number': 'A DRAWINGS',
            'line number': 'A.2'},}

        :param file_path: path to Excel file
        :return: 'Success' or 'Error'
        """
        try:
            string_for_start_row = content_of_excel_file_start_row
            self.dict_contents_of_file_by_section, self.dict_contents_of_file_by_file = read_from_excel_file(file_path, string_for_start_row)
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_file_by_section)
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_file_by_file)
            append_a_string_to_txt_file(self.location_of_log_file,'Successfully exported excel dicts to txt file (see above)')
            return 'Success'
        except Exception as e:
            print(e)
            self._log_error_and_return(e)

    def step_3_create_folders_in_finished_dir(self, finished_dir):
        """
        Creates folders in finished dir according to the structure of the Excel file
        :param finished_dir: path to finished dir
        :return: Success or Error
        """
        try:
            for key in self.dict_contents_of_file_by_section.keys():
                current_folder_path = os.path.join(finished_dir, key)

                if not directory_exists(current_folder_path):
                    # create_directory_with_dotnet(current_folder_path)
                    create_directory(current_folder_path)

            append_a_string_to_txt_file(self.location_of_log_file, 'Successfully created folders in finished dir')
            return 'Success'
        except Exception as e:
            self._log_error_and_return(e)

    def step_4_scan_finished_dir(self, finished_dir):
        """
        Scans the finished directory, fills-in a dict and exports the result to a txt file

        example folder: "MC077-022-001-Leak proof joint design and drawing for tank and deck surface"


        self.dict_contents_of_finished_dir:
        {'MC077-021-001 Leak proof joint design and drawing for hull': {
            'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull',
            'files': {
                'MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf': {
                    'number': 'MC077-021-001',
                    'name': 'Leak proof joint design and drawing for hull',
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf'},
                'MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg': {
                    'number': 'MC077-021-001',
                    'name': 'Leak proof joint design and drawing for hull',
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg'}}},

        Note: file_name is None if the actual file name is using the new format, i.e.
        „MC077-022-001_ 30092023-A1.pdf“
        instead of
        „MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf“
        first a search is performed for the old format, then for the new one:
            'files': {
                'MC077-021-001_28092023.dwg': {
                    'number': 'MC077-021-001',
                    'name': None,
                    'date': '28092023',
                    'path': 'C:\\Users\\User\\Desktop\\MK\\P\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001_28092023.dwg'},


        :param finished_dir: path to finished dir
        :return: 'Success' or 'Error'
        """
        # scan finished directory
        try:
            self.dict_contents_of_finished_dir = the_walk_loop('finished_dir', finished_dir)
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_finished_dir)
            append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported finished dir to txt file (see above)')

            return 'Success'
        except Exception as e:
            self._log_error_and_return(e)

    # ----------------------------------------------------------------------------------------
    # Comparators
    # ----------------------------------------------------------------------------------------
    def step_5_compare_ready_to_finished(self):
        """
        Compares the contents of ready and finished directories and creates a dict with the new folders waiting to be moved

        this dict is with empty folder destination path and empty file destination path
        self.dict_waiting_for_execution (before the correction, which comes after checking the Excel file):
        {'MC077-022-001 Leak proof joint design and drawing for tank and deck surface': {
            'folder destination path': '',
            'files_to_move': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg',
                    'destination path': '',
                    'number name': 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'},
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-099-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf',
                    'destination path': '',
                    'number name': 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'}}}

        self.dict_of_files_to_be_archived:
        {'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg': {
            'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg'}}

        :return: 'Success' + info or 'Error'
        """
        # -----------------------------------------------------------------------------------------
        # Part A: set of files to be copied
        # -----------------------------------------------------------------------------------------

        # temp set of files to be copied
        """
        {
            'MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg', 
            'MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf', 
            'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg', 
            'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf'
        }
        """
        set_of_files_to_be_copied = set()

        # dict of files to be archived, initialized to empty
        self.dict_of_files_to_be_archived = {}

        # ---------------------------------folders--------------------------------------
        # start with iterating ready since there may be folders absent in finished
        for ready_folder_number_name, ready_folder_data_dict in self.dict_contents_of_ready_dir.items():

            # check if finished is empty
            if len(self.dict_contents_of_finished_dir) == 0:

                # -------------------------------files---------------------------------------------
                # then iterate over the files in ready to add them all to the list of files to be copied
                for ready_file, ready_file_data_dict in ready_folder_data_dict['files'].items():

                    # add the file to the list of files to be copied
                    set_of_files_to_be_copied.add(ready_file)

                continue

            # -------------------------------folders---------------------------------------------
            # if not empty, iterate over the finished folders to compare with the selected ready folder
            for finished_folder_number_name, finished_folder_data_dict in self.dict_contents_of_finished_dir.items():

                # check if there is such a folder `number name` in finished
                if ready_folder_number_name == finished_folder_number_name:

                    # -------------------------------files---------------------------------------------
                    # then iterate over the files in ready
                    for ready_file, ready_file_data_dict in ready_folder_data_dict['files'].items():

                        # check if there are files in this finished sub-folder
                        if len(finished_folder_data_dict['files']) == 0:

                            # add the file to the list of files to be copied
                            set_of_files_to_be_copied.add(ready_file)

                            continue

                        # if not empty, iterate over the files in finished to compare with the selected ready file
                        for finished_file, finished_file_data_dict in finished_folder_data_dict['files'].items():

                            # get the extensions
                            ready_file_extension, finished_file_extension = os.path.splitext(ready_file)[1], os.path.splitext(finished_file)[1]

                            # check if the name and number of the 2 files match
                            if compare_by_name_and_number(ready_file_data_dict['name'],
                                                          ready_file_data_dict['number'],
                                                          finished_file_data_dict['name'],
                                                          finished_file_data_dict['number']):

                                # check if the extensions is different
                                if ready_file_extension != finished_file_extension:
                                    continue

                                # if they match, then check if the date of the ready file is newer
                                if ready_file_data_dict['date'] > finished_file_data_dict['date']:

                                    # add the file to the list of files to be copied
                                    set_of_files_to_be_copied.add(ready_file)

                                    # add the file to archive
                                    self.dict_of_files_to_be_archived[finished_file] = {
                                        'path': finished_file_data_dict['path']
                                    }

                            # if the name and number of the 2 files do not match
                            else:

                                # only if this is the last file in finished sub-folder
                                if finished_file == list(finished_folder_data_dict['files'].keys())[-1]:

                                    # add the file to the list of files to be copied
                                    set_of_files_to_be_copied.add(ready_file)

                    # -------------------------------folders---------------------------------------------
                # if `number name` of the folders do not match
                else:

                    # only if there is no such folder in finished
                    # ToDo: 5. Fixed this since was returning empty dict
                    # if finished_folder_number_name not in self.dict_contents_of_finished_dir.keys():
                    if ready_folder_number_name not in self.dict_contents_of_finished_dir.keys():

                        # -------------------------------files---------------------------------------------
                        # then iterate over the files in ready to add them all to the list of files to be copied
                        for ready_file, ready_file_data_dict in ready_folder_data_dict['files'].items():

                            # add the file to the list of files to be copied
                            set_of_files_to_be_copied.add(ready_file)

        # -----------------------------------------------------------------------------------------
        # Part B: fill-in the dict_waiting_for_execution based on the set of files to be copied
        # -----------------------------------------------------------------------------------------
        # reinitialize the dictionary to be empty
        self.dict_waiting_for_execution = {}

        # iterate over the set of files to be copied
        for set_file in set_of_files_to_be_copied:

            # iterate over the folders in ready
            for ready_folder_number_name, ready_folder_data_dict in self.dict_contents_of_ready_dir.items():

                # iterate over the files in ready
                for ready_file, ready_file_data_dict in ready_folder_data_dict['files'].items():

                    # check if the file is in ready
                    if set_file == ready_file:

                        # check if the folder is already in the dictionary
                        if ready_folder_number_name not in self.dict_waiting_for_execution:
                            self.dict_waiting_for_execution[ready_folder_number_name] = {}
                            self.dict_waiting_for_execution[ready_folder_number_name]['folder destination path'] = ''
                            self.dict_waiting_for_execution[ready_folder_number_name]['files_to_move'] = {}
                            self.dict_waiting_for_execution[ready_folder_number_name]['files_to_archive'] = {}

                        # add the file to move
                        self.dict_waiting_for_execution[ready_folder_number_name]['files_to_move'][ready_file] = {
                            'source path': ready_file_data_dict['path'],
                            'destination path': '',
                            # ToDo: 4. Changed this
                            # 'number name': ready_file_data_dict['number'] + ' ' + ready_file_data_dict['name']
                            'number name': ready_folder_number_name
                        }

                        # break the loop
                        break

        # -----------------------------------------------------------------------------------------
        # Part C: prepare the info about new folders to return
        # -----------------------------------------------------------------------------------------
        if len(self.dict_waiting_for_execution) > 0:
            info = f"Бр. обновени папки в Ready спрямо Finished: {len(self.dict_waiting_for_execution)}\n"
            count = 1
            for key, value in self.dict_waiting_for_execution.items():
                folder_name = self.dict_contents_of_ready_dir[key]['path']
                final_name = extract_text_after_last_backslash(folder_name)
                info += f"{count}) {final_name}\n"
                count += 1

        else:
            info = None

        # -----------------------------------------------------------------------------------------
        # Part D: export to txt file
        # -----------------------------------------------------------------------------------------
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_waiting_for_execution)
            append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported dict_waiting_for_execution (before correction) to txt file (see above)')
            return 'Success', info
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', e

    def step_6_check_if_new_folders_in_work_and_their_contents_correspond_to_excel(self, finished_dir):
        """
        Checks if the dict waiting for execution corresponds to the Excel file and then also after
        scanning the pdf files. Corrects the dict_waiting_for_execution and exports the result to a txt file

        :param finished_dir: path to finished dir

        adds the folder destination path if empty and the file destination path if empty!
        self.dict_waiting_for_execution (after correction after checking the Excel file):

        {'MC077-022-001 Leak proof joint design and drawing for tank and deck surface': {
            'folder destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
            'files_to_move': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg',
                    'destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
                    'number name': 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'}},
            'files_to_archive': {}},

        :return: 'Success' + info or 'Error'
        """
        return_info = ""
        key_to_remove = []
        files_to_remove = {}

        # check if the folders in waiting for execution correspond to contents of Excel file
        for key, value in self.dict_waiting_for_execution.items():
            not_found_and_needs_to_be_removed = True

            # check if the folder is in the Excel file
            for key2, value2 in self.dict_contents_of_file_by_file.items():

                # check if match
                if key.lower() == key2.lower():
                    not_found_and_needs_to_be_removed = False

                    # fills folder destination path if empty
                    if value['folder destination path'] == '':

                        new_path = os.path.join(
                            finished_dir,
                            value2['section number'],
                            key.replace(' ', '-', 1)    # include a dash instead of a space
                        )

                        new_path = normalize_path_to_have_only_forward_slashes(new_path)

                        # update folder destination path
                        value['folder destination path'] = new_path

                        # update all files with empty destination path
                        for key3, value3 in value['files_to_move'].items():

                            if value3['destination path'] == '':
                                value3['destination path'] = value['folder destination path']

                    # check if the files аre in the Excel file
                    for key4, value4 in value['files_to_move'].items():

                        remove_file = True
                        number_name = value4['number name']
                        file_path = value4['source path']

                        for key5, value5 in self.dict_contents_of_file_by_file.items():

                            if number_name.lower() == key5.lower():

                                # ToDo: 17.04.2024: commented for now to skip installation of pytesseract
                                # now scan the PDF ------------------------------------------------
                                # try:
                                #     file_extension = os.path.splitext(key4)[1]
                                #     if file_extension == '.pdf':
                                #         project_name, project_description, document_number = (
                                #             self._scan_pdf(file_path, self.pdf_scanning_coordinates))
                                #         return_info += f"--- Номер на документ: {document_number}\n"
                                #         return_info += f"--- Описание на проект: {project_description}\n"
                                #         return_info += f"--- Име на проект: {project_name}\n"
                                #
                                #         # check for match
                                #         if compare_by_name_and_number(
                                #                 project_description,
                                #                 document_number,
                                #                 ' '.join(number_name.split(' ')[1:]),
                                #                 number_name.split(' ')[0]
                                #         ):
                                #             return_info += f"--- Съответства на Excel файла\n"
                                #         else:
                                #             return_info += f"--- НЕ съответства на Excel файла\n"
                                # except Exception as e:
                                #     return_info += f"Неуспешно сканиране на PDF файла: {e}\n"

                                remove_file = False
                                break

                        if remove_file:
                            if key not in files_to_remove:
                                files_to_remove[key] = []

                            files_to_remove[key].append(key4)

                    break

            # if the folder is not in the Excel file, remove it from waiting for execution
            if not_found_and_needs_to_be_removed:
                key_to_remove.append(key)

        # remove folders from waiting for execution, which are not matching the Excel file
        for key in key_to_remove:
            return_info += f"Папката {key} НЕ съответства на Excel файла\n"
            del self.dict_waiting_for_execution[key]

        # remove files from waiting for execution, which are not matching the Excel file
        for key, value in files_to_remove.items():
            for file in value:
                return_info += f"Файлът {file} НЕ съответства на Excel файла\n"
                del self.dict_waiting_for_execution[key]['files_to_move'][file]

        try:
            append_a_string_to_txt_file(self.location_of_log_file, return_info)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', None

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully compared new folders in work compared to ready with Excel (see above)')

        return 'Success', return_info

    @staticmethod
    def _scan_pdf(file_path, pdf_scanning_coordinates):
        """
        Scans the pdf file and returns the project name, project description and document number
        :param file_path: the path to the pdf file
        :param pdf_scanning_coordinates: the coordinates for scanning the pdf files
        :return: project name, project description, document number
        """
        # split pdf_scanning_coordinates
        project_name_coordinates, project_description_coordinates, document_number_coordinates = (
            split_pdf_scanning_coordinates(pdf_scanning_coordinates))

        # scan project name
        project_name = extract_text_from_pdf(file_path, project_name_coordinates)

        # scan project description
        project_description = extract_text_from_pdf(file_path, project_description_coordinates)

        # scan document number
        document_number = extract_text_from_pdf(file_path, document_number_coordinates)

        return project_name, project_description, document_number

    # ----------------------------------------------------------------------------------------
    # Moving
    # ----------------------------------------------------------------------------------------
    def step_7_archive_then_new_folders_from_ready_to_finished(self, source_folder, destination_folder, archive_folder):
        """
        Archives the files in the folders in the ready dir and then moves the folders to the finished dir
        :param source_folder: path to source folder
        :param destination_folder: path to destination folder
        :param archive_folder: path to archive folder
        :return: 'Success' or 'Error'
        """
        list_of_archive_paths = []
        """
        this list keeps the paths of the files to be archived not to create 2 archive folders 
        inside the same path in 1 button click
        """

        # -------------------------------------------------------------------------------
        # Part A: Create archive sub-dirs and move the files there
        # -------------------------------------------------------------------------------
        # iterate over the dict_of_files_to_be_archived
        for file_to_be_archived, file_to_be_archived_data_dict in self.dict_of_files_to_be_archived.items():

            # get the path of the file
            file_to_be_archived_path = file_to_be_archived_data_dict['path']

            # get the path of the folder
            folder_to_be_archived_path = os.path.dirname(file_to_be_archived_path)

            current_datetime = datetime.now()
            folder_name = current_datetime.strftime("%y%m%d%H%M%S")     # 231123125228, which is 23.11.2023 12:52:28
            path_of_new_archive = os.path.join(folder_to_be_archived_path, folder_name)

            # create the folder if the file path is not in the list of archive paths
            if path_of_new_archive not in list_of_archive_paths:
                create_directory(path_of_new_archive)

                # add the path to the list of archive paths
                list_of_archive_paths.append(path_of_new_archive)

            # move the file to archive there
            move_directory(file_to_be_archived_path, path_of_new_archive)

            # ToDo: temp length fix, remove only this when length of dirs is reduced, 6. removed temp fix
            # -------------------------------------------------------------------------------
            # rename the files
            # counter = 1
            # for file in os.listdir(path_of_new_archive):
            #     file_path = os.path.join(path_of_new_archive, file)
            #
            #     # get the extension
            #     current_file_name = os.path.basename(file)
            #     file_extension = os.path.splitext(file)[1]
            #
            #     # rename the file
            #     new_file_name = str(counter) + file_extension
            #     os.rename(file_path, os.path.join(path_of_new_archive, new_file_name))
            #
            #     counter += 1
            # -------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------
        # Part B: Archive the archive sub-dirs and delete them
        # -------------------------------------------------------------------------------
        # iterate over the list of archive paths
        for archive_sub_dir_path in list_of_archive_paths:

            # get the path to place the archive in
            archive_path = os.path.dirname(archive_sub_dir_path)
            archive_directory(archive_sub_dir_path, archive_path)

            # delete the folder
            delete_directory(archive_sub_dir_path)

        # -------------------------------------------------------------------------------
        # Part C: Move the files
        # -------------------------------------------------------------------------------
        # iterate over the dict_waiting_for_execution
        for ready_folder_number_name, ready_folder_data_dict in self.dict_waiting_for_execution.items():

            # iterate over the files_to_move
            for file_to_move, file_to_move_data_dict in ready_folder_data_dict['files_to_move'].items():

                # get the file name
                file_name = os.path.basename(file_to_move)

                # get the source path (path of the file + file name and extension)
                source_path = file_to_move_data_dict['source path']

                # replace `Ready` with `READY` in the source path
                source_path = source_path.replace('Ready', 'READY')

                # get the destination path (path of the folder + file name and extension)
                destination_path = file_to_move_data_dict['destination path'] + '\\' + file_name

                # check if the destination path exists
                if not os.path.exists(file_to_move_data_dict['destination path']):
                    create_directory(file_to_move_data_dict['destination path'])

                # move the file
                # copy_file_with_dotnet(source_path, destination_path)
                copy_file(source_path, destination_path)

        return 'Success'

    # ----------------------------------------------------------------------------------------
    # General support
    # ----------------------------------------------------------------------------------------
    def _print_all_current_contents(self):
        """
        Prints the contents of all the structures
        """
        print(f"Now in Ready: {self.dict_contents_of_ready_dir}")
        print(f"Now in Finished: {self.dict_contents_of_finished_dir}")
        print(f"Now in Saved Ready: {self.contents_of_saved_ready_dir}")
        print(f"Main names: {self.list_of_created_main_folder_names}")

    def _log_error_and_return(self, e):
        """
        Logs the error and returns it
        :param e: the error message
        :return: the error message
        """
        append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
        return f'Error: {e}'
