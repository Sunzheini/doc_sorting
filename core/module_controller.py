# -*- coding: utf-8 -*-
import os
from datetime import datetime

from support.comparators import compare_by_name_and_number
from support.pdf_scanner import extract_text_from_pdf, split_pdf_scanning_coordinates
from support.excel_reader import read_from_excel_file
from core.walk_loop_ready import the_walk_loop_ready
from core.walk_loop_finished import the_walk_loop_finished
from support.constants import content_of_excel_file_start_row
from support.folder_and_file_manager import create_directory, directory_exists, archive_directory, delete_directory, \
    move_directory, copy_file
from support.folder_and_file_manager_dotnet import (create_directory_with_dotnet, delete_directory_with_dotnet,
                                                    move_directory_with_dotnet, delete_file_with_dotnet)
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
        self.dict_waiting_for_execution = None          # filled-in by step_5_compare_ready_to_finished
        # the last one is then corrected by step_6_check_if_new_folders_in_work_and_their_contents_correspond_to_excel

    # ----------------------------------------------------------------------------------------
    # Scanners
    # ----------------------------------------------------------------------------------------
    def step_1_scan_ready_dir(self, ready_dir):
        """
        Scans the ready directory, fills-in a dict and exports the result to a txt file

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

        :param ready_dir: path to ready dir
        :return: 'Success' or 'Error'
        """
        try:
            self.dict_contents_of_ready_dir = the_walk_loop_ready(ready_dir)
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
                    create_directory_with_dotnet(current_folder_path)

            append_a_string_to_txt_file(self.location_of_log_file, 'Successfully created folders in finished dir')
            return 'Success'
        except Exception as e:
            self._log_error_and_return(e)

    def step_4_scan_finished_dir(self, finished_dir):
        """
        Scans the finished directory, fills-in a dict and exports the result to a txt file

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

        Currently: 'MC077-021-001 Leak proof joint design and drawing for hull'
        is:        'MC077-021-001'      because of the error

        :param finished_dir: path to finished dir
        :return: 'Success' or 'Error'
        """
        # scan finished directory
        try:
            self.dict_contents_of_finished_dir = the_walk_loop_finished(finished_dir)
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

        self.dict_waiting_for_execution (before correction after checking the Excel file):
        {'MC077-022-001 Leak proof joint design and drawing for tank and deck surface': {
            'folder destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
            'files_to_move': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg',
                    'destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
                    'number name': 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'},
                'MC077-022-099-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-099-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf',
                    'destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
                    'number name': 'MC077-022-099 Leak proof joint design and drawing for tank and deck surface'}},
            'files_to_archive': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg': {
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg'}}}}

        Currently the dest path contains not:   'MC077-021-001 Leak proof joint design and drawing for hull'
        but:                                    'MC077-021-001'      because of the error

        :return: 'Success' + info or 'Error'
        """
        # reinitialize the dictionary to be empty
        self.dict_waiting_for_execution = {}

        # compare self.dict_contents_of_ready_dir and self.dict_contents_of_finished_dir
        for key, value in self.dict_contents_of_ready_dir.items():
            this_key_needs_to_be_moved = True
            iteration_is_finished = False

            # check if the finished dir is empty
            if len(self.dict_contents_of_finished_dir) == 0:
                # check if the folder is already in the dictionary
                if key not in self.dict_waiting_for_execution:
                    self.dict_waiting_for_execution[key] = {}
                    self.dict_waiting_for_execution[key]['folder destination path'] = ''
                    self.dict_waiting_for_execution[key]['files_to_move'] = {}
                    self.dict_waiting_for_execution[key]['files_to_archive'] = {}

                # lists of files in ready
                dict_of_ready_files = value['files']

                # iterate over the files in ready
                for ready_file in dict_of_ready_files:
                    ready_file_path = dict_of_ready_files[ready_file]['path']
                    ready_file_number = dict_of_ready_files[ready_file]['number']
                    ready_file_name = dict_of_ready_files[ready_file]['name']

                    # add the file to move
                    self.dict_waiting_for_execution[key]['files_to_move'][ready_file] = {
                        'source path': ready_file_path,
                        'destination path': '',
                        'number name': ready_file_number + ' ' + ready_file_name
                    }
                continue

            # ------------------------------------------------------------
            # ToDo: added since the finished dir is with number only
            # for finished_key in self.dict_contents_of_finished_dir.keys():
            #     # check if it is the last finished_key
            #     if finished_key == list(self.dict_contents_of_finished_dir.keys())[-1]:
            #         iteration_is_finished = True
            #
            #     # check for matching
            #     part_key = key[:13]
            #     if part_key in finished_key:
            #         this_key_needs_to_be_moved = False

            # ------------------------------------------------------------
            # ToDo: commented
            # check for matching
            if key in self.dict_contents_of_finished_dir.keys():

            # ------------------------------------------------------------
            # ToDO: changed indentation with 1 tab up to the right to the line below for the bug

                # lists of files in ready and finished
                dict_of_ready_files = value['files']
                # ToDo: changed key to key[:13]
                dict_of_finished_files = self.dict_contents_of_finished_dir[key]['files']
                # dict_of_finished_files = self.dict_contents_of_finished_dir[key[:13]]['files']

                # folder destination path for later
                # ToDo: changed key to key[:13]
                folder_destination_path = self.dict_contents_of_finished_dir[key]['path']
                # folder_destination_path = self.dict_contents_of_finished_dir[key[:13]]['path']

                # iterate over the files in ready
                for ready_file in dict_of_ready_files:
                    not_found_and_must_be_moved = True

                    ready_file_number = dict_of_ready_files[ready_file]['number']
                    ready_file_name = dict_of_ready_files[ready_file]['name']
                    ready_file_date = dict_of_ready_files[ready_file]['date']
                    ready_file_path = dict_of_ready_files[ready_file]['path']
                    ready_file_extension = os.path.splitext(ready_file)[1]

                    # iterate over the files in finished
                    for finished_file in dict_of_finished_files:
                        finished_file_number = dict_of_finished_files[finished_file]['number']
                        finished_file_name = dict_of_finished_files[finished_file]['name']
                        finished_file_date = dict_of_finished_files[finished_file]['date']
                        finished_file_path = dict_of_finished_files[finished_file]['path']
                        finished_file_extension = os.path.splitext(finished_file)[1]

                        # check for matching number, name and extension
                        if (ready_file_number == finished_file_number
                                and ready_file_name == finished_file_name
                                and ready_file_extension == finished_file_extension):

                            not_found_and_must_be_moved = False

                            # check if the date is newer
                            if ready_file_date > finished_file_date:

                                # check if the folder is already in the dictionary
                                if key not in self.dict_waiting_for_execution:
                                    self.dict_waiting_for_execution[key] = {}
                                    self.dict_waiting_for_execution[key]['folder destination path'] = folder_destination_path
                                    self.dict_waiting_for_execution[key]['files_to_move'] = {}
                                    self.dict_waiting_for_execution[key]['files_to_archive'] = {}

                                # add the file to move
                                self.dict_waiting_for_execution[key]['files_to_move'][ready_file] = {
                                    'source path': ready_file_path,
                                    'destination path': folder_destination_path,
                                    'number name': ready_file_number + ' ' + ready_file_name
                                }

                                # add the file to archive
                                self.dict_waiting_for_execution[key]['files_to_archive'][finished_file] = {
                                    'path': finished_file_path
                                }

                                # break the loop
                                break

                    # add to the folder to move
                    if not_found_and_must_be_moved:
                        # check if the folder is already in the dictionary
                        if key not in self.dict_waiting_for_execution:
                            self.dict_waiting_for_execution[key] = {}
                            self.dict_waiting_for_execution[key]['folder destination path'] = folder_destination_path
                            self.dict_waiting_for_execution[key]['files_to_move'] = {}
                            self.dict_waiting_for_execution[key]['files_to_archive'] = {}

                        # add the file to move
                        self.dict_waiting_for_execution[key]['files_to_move'][ready_file] = {
                            'source path': ready_file_path,
                            'destination path': folder_destination_path,
                            'number name': ready_file_number + ' ' + ready_file_name
                        }

            # if the folder is not in finished, add it to dict_waiting_for_execution
            else:
                if iteration_is_finished:
                    if this_key_needs_to_be_moved:

                        # folder destination path for later
                        folder_destination_path = ''

                        # check if the folder is already in the dictionary
                        if key not in self.dict_waiting_for_execution:
                            self.dict_waiting_for_execution[key] = {}
                            self.dict_waiting_for_execution[key]['folder destination path'] = folder_destination_path
                            self.dict_waiting_for_execution[key]['files_to_move'] = {}
                            self.dict_waiting_for_execution[key]['files_to_archive'] = {}

                        # lists of files in ready
                        dict_of_ready_files = value['files']

                        # iterate over the files in ready
                        for ready_file in dict_of_ready_files:
                            ready_file_path = dict_of_ready_files[ready_file]['path']
                            ready_file_number = dict_of_ready_files[ready_file]['number']
                            ready_file_name = dict_of_ready_files[ready_file]['name']

                            # add the file to move
                            self.dict_waiting_for_execution[key]['files_to_move'][ready_file] = {
                                'source path': ready_file_path,
                                'destination path': folder_destination_path,
                                'number name': ready_file_number + ' ' + ready_file_name
                            }

            # ------------------------------------------------------------

        # prepare the info about new folders to return
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

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_waiting_for_execution)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', None

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported dict_waiting_for_execution (before correction) to txt file (see above)')

        return 'Success', info

    def _log_step(self, text):
        append_a_string_to_txt_file(self.location_of_log_file, text)

    def step_6_check_if_new_folders_in_work_and_their_contents_correspond_to_excel(self, finished_dir):
        """
        Checks if the dicting waiting for execution corresponds to the Excel file and then also after
        scanning the pdf files. Corrects the dict_waiting_for_execution and exports the result to a txt file

        :param finished_dir: path to finished dir

        self.dict_waiting_for_execution (after correction after checking the Excel file):
        {'MC077-022-001 Leak proof joint design and drawing for tank and deck surface': {
            'folder destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
            'files_to_move': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg': {
                    'source path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg',
                    'destination path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001',
                    'number name': 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'}},
            'files_to_archive': {
                'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg': {
                    'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\MC077-022-001\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg'}}}}

        Currently the dest path contains not:   'MC077-021-001 Leak proof joint design and drawing for hull'
        but:                                    'MC077-021-001'      because of the error

        :return: 'Success' + info or 'Error'
        """
        return_info = ""
        key_to_remove = []
        files_to_remove = {}

        self._log_step('1')

        # check if the folders in waiting for execution correspond to contents of Excel file
        for key, value in self.dict_waiting_for_execution.items():
            not_found_and_needs_to_be_removed = True

            self._log_step(f"key in waiting for execution: {key}")

            # check if the folder is in the Excel file
            for key2, value2 in self.dict_contents_of_file_by_file.items():

                self._log_step(f"key2 in Excel: {key2}")

                # check if match
                if key.lower() == key2.lower():
                    not_found_and_needs_to_be_removed = False

                    self._log_step("match")

                    # fills folder destination path if empty
                    if value['folder destination path'] == '':

                        self._log_step("folder destination path is empty")

                        new_path = os.path.join(
                            finished_dir,
                            value2['section number'],
                            key
                        )

                        new_path = normalize_path_to_have_only_forward_slashes(new_path)

                        # update folder destination path
                        value['folder destination path'] = new_path

                        # update all files with empty destination path
                        for key3, value3 in value['files_to_move'].items():

                            self._log_step(f"key3: {key3}")

                            if value3['destination path'] == '':
                                value3['destination path'] = value['folder destination path']

                    # check if the files аre in the Excel file
                    for key4, value4 in value['files_to_move'].items():

                        self._log_step(f"key4: {key4}")

                        remove_file = True
                        number_name = value4['number name']
                        file_path = value4['source path']

                        for key5, value5 in self.dict_contents_of_file_by_file.items():

                            self._log_step(f"key5: {key5}")

                            if number_name.lower() == key5.lower():

                                self._log_step("match")

                                # now scan the Excel ------------------------------------------------
                                try:
                                    file_extension = os.path.splitext(key4)[1]
                                    if file_extension == '.pdf':
                                        project_name, project_description, document_number = (
                                            self._scan_pdf(file_path, self.pdf_scanning_coordinates))
                                        return_info += f"--- Номер на документ: {document_number}\n"
                                        return_info += f"--- Описание на проект: {project_description}\n"
                                        return_info += f"--- Име на проект: {project_name}\n"

                                        # check for match
                                        if compare_by_name_and_number(
                                                project_description,
                                                document_number,
                                                ' '.join(number_name.split(' ')[1:]),
                                                number_name.split(' ')[0]
                                        ):
                                            return_info += f"--- Съответства на Excel файла\n"
                                        else:
                                            return_info += f"--- НЕ съответства на Excel файла\n"
                                except Exception as e:
                                    return_info += f"Неуспешно сканиране на PDF файла: {e}\n"

                                remove_file = False
                                break

                        if remove_file:
                            if key not in files_to_remove:
                                files_to_remove[key] = []

                            files_to_remove[key].append(key4)

                    break

            # if the folder is not in the Excel file, remove it from waiting for execution
            if not_found_and_needs_to_be_removed:
                self._log_step("not found and needs to be removed")

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
        # archive files inside the folders
        for key, value in self.dict_waiting_for_execution.items():
            # create archive folder
            # ToDO: does not work
            # archive_folder_path = self.dict_waiting_for_execution[key]['folder destination path']
            # new_path = normalize_path_to_have_only_forward_slashes(archive_folder_path)
            # print(f"Archive Folder Path: {new_path}")

            # # ToDo: this works
            # new_path = r"C:\Users\User\Desktop\MK\ProjectXYZ\05 DESIGN DOCUMENTS\020 CLASSIFICATION DRAWINGS\A DRAWINGS\Archive"

            # ToDo: this works
            # old = normalize_path_to_have_only_forward_slashes(self.dict_waiting_for_execution[key]['folder destination path'])
            # explode = old.split('\\')
            #
            # explode_2 = 'A DRAWINGS'
            # # explode_1 = 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface'
            # explode_1 = 'MC077-022-001'
            #
            # # new_path = os.path.join(archive_folder, explode[-2], explode[-1])
            # new_path = os.path.join(archive_folder, explode_2, explode_1)

            archive_folder_path = self.dict_waiting_for_execution[key]['folder destination path']
            new_path = normalize_path_to_have_only_forward_slashes(archive_folder_path)

            # ------------------------------------------------------------
            # ToDo: this part is for the bug, comment only this if bug is solved
            # explode = new_path.split('\\')
            # explode_2 = explode[-2]
            # explode_1 = explode[-1][:13]
            # new_path = os.path.join(archive_folder, explode_2, explode_1)
            # ------------------------------------------------------------

            # # Check if the folder exists, create it if not
            if not directory_exists(new_path):
                create_directory_with_dotnet(new_path)

            # archive the files in files_to_archive
            if len(value['files_to_archive']) > 0:

                # get current date and time
                current_datetime = datetime.now()
                folder_name = current_datetime.strftime("%y%m%d%H%M%S")   # 231123125228, which is 23.11.2023 12:52:28

                # create the folder
                path_of_new_archive = os.path.join(new_path, folder_name)
                create_directory_with_dotnet(path_of_new_archive)

                # move the files to archive there
                for key2, value2 in value['files_to_archive'].items():
                    move_directory_with_dotnet(value2['path'], path_of_new_archive)

                # archive the folder
                archive_directory(path_of_new_archive, new_path)

                # delete the folder
                delete_directory_with_dotnet(path_of_new_archive)

            # Now proceed with copying the files
            for key2, value2 in value['files_to_move'].items():
                # copy the file to the archive folder
                copy_file(value2['source path'], new_path)

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
