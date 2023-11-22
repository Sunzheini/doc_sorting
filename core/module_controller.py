# -*- coding: windows-1251 -*-

import os
import shutil
import zipfile
import re
from pathlib import Path

from support.custom_functions_lib import normalize_path_to_have_only_forward_slashes
from support.pdf_reader import extract_text_from_pdf
from support.excel_reader import read_from_excel_file
from support.get_info import the_walk_loop_ready, the_walk_loop_finished
from support.txt_writer import append_a_dict_to_txt_file, append_a_string_to_txt_file


class ModuleController:
    def __init__(
            self,
            location_of_log_file,
            db_controller,
            paths_table_name,
            previous_state_table_name,
            pdf_scanning_coordinates,
    ):
        self.location_of_log_file = location_of_log_file

        # database
        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        # structures
        self.dict_contents_of_ready_dir = None
        self.dict_contents_of_file_by_section = None
        self.dict_contents_of_file_by_file = None
        self.dict_contents_of_finished_dir = None
        self.dict_waiting_for_execution = None




        self.contents_of_saved_ready_dir = None

        self.list_of_created_main_folder_names = []
        self.dict_of_names_of_new_folders_in_ready_compared_to_finished_and_main_folder_names = {}

        self.new_folders_in_ready_compared_to_saved_ready = None

    # ----------------------------------------------------------------------------------------
    # Scanners
    # ----------------------------------------------------------------------------------------
    def scan_ready_dir(self, ready_dir):
        """
        Scans the ready directory and exports the result to a txt file
        :param ready_dir:
        :return: 'Success' or 'Error'
        """
        # scan ready directory
        try:
            self.dict_contents_of_ready_dir = the_walk_loop_ready(ready_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_ready_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported ready dir to txt file (see above)')
        return 'Success'

    def scan_excel(self, file_path):
        """
        Scans the Excel file and exports the result to a txt file
        :param file_path:
        :return: 'Success' or 'Error'
        """
        # define a string, by which the function determines the start row
        string_for_start_row = 'A'

        # read from Excel file
        try:
            self.dict_contents_of_file_by_section, self.dict_contents_of_file_by_file \
                = read_from_excel_file(file_path, string_for_start_row)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_file_by_section)
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_file_by_file)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported excel to txt file (see above)')
        return 'Success'

    def create_folders_in_finished_dir(self, finished_dir):
        """
        Creates folders in finished dir
        :param finished_dir:
        :return: Success or Error
        """
        for key in self.dict_contents_of_file_by_section.keys():
            current_folder_path = os.path.join(finished_dir, key)

            # check if the folder exists
            if not os.path.exists(current_folder_path):
                os.makedirs(current_folder_path)

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully created folders in finished dir')
        return 'Success'

    def scan_finished_dir(self, finished_dir):
        """
        Scans the finished directory and exports the result to a txt file
        :param finished_dir:
        :return: 'Success' or 'Error'
        """
        # scan finished directory
        try:
            self.dict_contents_of_finished_dir = the_walk_loop_finished(finished_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.dict_contents_of_finished_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported finished dir to txt file (see above)')
        return 'Success'

    def compare_ready_to_finished(self):
        """
        Compares the contents of ready and finished directories and exports the result to a txt file
        dict5 {'folder number folder name': {'folder destination path': '', 'files_to_move': {'number name', 'source path', 'destination path'}, 'files_to_archive': {'number name', 'path'}}}
        :return: 'Success' + info or 'Error'
        """
        # reinitialize the dictionary to be empty
        self.dict_waiting_for_execution = {}

        # compare self.dict_contents_of_ready_dir and self.dict_contents_of_finished_dir
        for key, value in self.dict_contents_of_ready_dir.items():

            # check for matching
            if key in self.dict_contents_of_finished_dir:

                # lists of files in ready and finished
                dict_of_ready_files = value['files']
                dict_of_finished_files = self.dict_contents_of_finished_dir[key]['files']

                # folder destination path for later
                folder_destination_path = self.dict_contents_of_finished_dir[key]['path']

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

        # prepare the info about new folder to return
        if len(self.dict_waiting_for_execution) > 0:
            info = f"Бр. обновени папки в Ready спрямо Finished: {len(self.dict_waiting_for_execution)}\n"
            count = 1
            for key, value in self.dict_waiting_for_execution.items():
                folder_name = self.dict_contents_of_ready_dir[key]['path']
                final_name = self._extract_text_after_last_backslash(folder_name)
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
                                    'Successfully exported new folders in ready to txt file (see above)')
        return 'Success', info

    def _scan_pdf(self, file_path, pdf_scanning_coordinates):
        # split pdf_scanning_coordinates
        project_name_coordinates, project_description_coordinates, document_number_coordinates = (
            self._split_pdf_scanning_coordinates(pdf_scanning_coordinates))

        # scan project name
        project_name = extract_text_from_pdf(file_path, project_name_coordinates)

        # scan project description
        project_description = extract_text_from_pdf(file_path, project_description_coordinates)

        # scan document number
        document_number = extract_text_from_pdf(file_path, document_number_coordinates)

        return project_name, project_description, document_number

    def check_if_new_folders_in_work_and_their_contents_correspond_to_excel(self, finished_dir):
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
                            key
                        )

                        new_path = normalize_path_to_have_only_forward_slashes(new_path)

                        # update folder destination path
                        value['folder destination path'] = new_path

                        # updated all files with empty destination path
                        for key3, value3 in value['files_to_move'].items():
                            if value3['destination path'] == '':
                                value3['destination path'] = value['folder destination path']

                    # # check if the files аre in the Excel file
                    for key4, value4 in value['files_to_move'].items():
                        remove_file = True
                        number_name = value4['number name']
                        file_path = value4['source path']

                        for key5, value5 in self.dict_contents_of_file_by_file.items():
                            if number_name.lower() == key5.lower():

                                # now scan the Excel ------------------------------------------------
                                file_extension = os.path.splitext(key4)[1]
                                if file_extension == '.pdf':
                                    project_name, project_description, document_number = (
                                        self._scan_pdf(file_path, self.pdf_scanning_coordinates))
                                    return_info += f"--- Номер на документ: {document_number}\n"
                                    return_info += f"--- Описание на проект: {project_description}\n"
                                    return_info += f"--- Име на проект: {project_name}\n"

                                    # check for match
                                    if self._compare_by_name_and_number(
                                        project_description,
                                        document_number,
                                        ' '.join(number_name.split(' ')[1:]),
                                        number_name.split(' ')[0]
                                    ):
                                        return_info += f"--- Съответства на Excel файла\n"
                                    else:
                                        return_info += f"--- НЕ съответства на Excel файла\n"

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

    # ----------------------------------------------------------------------------------------
    # Moving
    # ----------------------------------------------------------------------------------------
    def _archive_folder(self, path_of_folder_to_archive, archive_folder):
        # Create an archive of the folder
        folder_name = self._extract_text_after_last_backslash(path_of_folder_to_archive)
        archive_name = folder_name + ".zip"
        archive_path = os.path.join(archive_folder, archive_name)

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for root, dirs, files in os.walk(path_of_folder_to_archive):
                for file in files:
                    archive.write(os.path.join(root, file), os.path.join(folder_name, file))

    def archive_then_new_folders_from_ready_to_finished(self, source_folder, destination_folder, archive_folder):
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
            explode = new_path.split('\\')
            explode_2 = explode[-2]
            explode_1 = explode[-1][:13]
            new_path = os.path.join(archive_folder, explode_2, explode_1)

            # # Check if the folder exists, create it if not
            if not os.path.exists(new_path):
                os.makedirs(new_path)

            # ToDo: up to the archiving
            # # archive the files in files_to_archive
            # for key2, value2 in value['files_to_archive'].items():
            #     # archive the file
            #     self._archive_folder(value2['path'], new_path)

            # ToDo: this works, but when i had existing 20230928 folder it didnt create ot copy
            # Now proceed with copying the files
            for key2, value2 in value['files_to_move'].items():
                # copy the file to the archive folder
                shutil.copy(value2['source path'], new_path)

        return 'Success'







    def _create_list_of_main_folder_names(self):
        self.list_of_created_main_folder_names = []

        # create folders in finished dir
        for key, value in self.dict_contents_of_file_by_section.items():
            current_folder_name = key

            # remove last characters separated by space
            current_folder_name = current_folder_name.rsplit(' ', 1)[0]

            # check if the folder exists
            if current_folder_name not in self.list_of_created_main_folder_names:
                self.list_of_created_main_folder_names.append(current_folder_name)
        # # create folders in finished dir
        # for key, value in self.contents_of_file.items():
        #     current_folder_name = key
        #
        #     # remove last characters separated by space
        #     current_folder_name = current_folder_name.rsplit(' ', 1)[0]
        #     current_folder_path = os.path.join(finished_dir, current_folder_name)
        #
        #     # check if the folder exists
        #     if not os.path.exists(current_folder_path):
        #         os.makedirs(current_folder_path)
        #         self.list_of_created_main_folder_names.append(current_folder_name)
        #
        # # return
        # append_a_string_to_txt_file(self.location_of_log_file,
        #                             'Successfully created folders in finished dir')
        #
        # return 'Success'

    def function4_extract_content_of_finished_dir_from_database(self):
        # Retrieve data from the database
        try:
            data = self.db_controller.retrieve_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # Fill the dictionary with the retrieved data
        try:
            self.contents_of_saved_ready_dir = {}
            for row in data:
                self.contents_of_saved_ready_dir[row[1]] = row[2]
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_saved_ready_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported saved work dir to txt file (see above)')
        return 'Success'

    # ----------------------------------------------------------------------------------------
    # Comparators
    # ----------------------------------------------------------------------------------------
    def _print_all_current_contents(self):
        print(f"Now in Ready: {self.dict_contents_of_ready_dir}")
        print(f"Now in Finished: {self.dict_contents_of_finished_dir}")
        print(f"Now in Saved Ready: {self.contents_of_saved_ready_dir}")
        print(f"Main names: {self.list_of_created_main_folder_names}")

    @staticmethod
    def _split_folder_name_into_date_number_name_revision(string):
        pattern = r'(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(?:\s*-\s*|\s*-|\s*-|-\s*)?((\d)?)'

        match = re.search(pattern, string)

        if match:
            date = match.group(1)
            number = match.group(3) + match.group(4) + '-' + match.group(6) + '-' + match.group(8)
            name = match.group(10)
            revision = match.group(11)

            if revision == "":
                revision = 0

            return date, number, name, revision
        else:
            return None, None, None, None

    @staticmethod
    def _split_file_name_into_number_name(string):
        pattern = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'

        match = re.search(pattern, string)

        if match:
            number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
            name = match.group(8)

            return number, name
        else:
            return None, None

    @staticmethod
    def _extract_text_after_last_backslash(path):
        # Use a regular expression to extract the text after the last backslash
        pattern = r'[^\\]+$'
        match = re.search(pattern, path)
        name = match.group(0)
        return name

    @staticmethod
    def _compare_by_name_and_number(name1, number1, name2, number2):
        # turn to lowercase
        name1 = name1.lower()
        name2 = name2.lower()

        if name1 != name2:
            return False
        if number1 != number2:
            return False
        return True

    @staticmethod
    def _split_pdf_scanning_coordinates(pdf_scanning_coordinates):
        project_name_coordinates = pdf_scanning_coordinates['project_name']
        project_description_coordinates = pdf_scanning_coordinates['project_description']
        document_number_coordinates = pdf_scanning_coordinates['document_number']

        return project_name_coordinates, project_description_coordinates, document_number_coordinates

    # ToDo: currently this is working by adding the folders 1 by 1 from source to work_dir and clicking the button1
    def function5_new_folders_in_ready_compared_to_saved_ready(self):
        # prints contents of the 3 sources
        self._print_all_current_contents()

        self.new_folders_in_ready_compared_to_saved_ready = {}
        for key, value in self.dict_contents_of_ready_dir.items():
            not_found = True
            work_date, work_number, work_name, work_revision = (
                self._split_folder_name_into_date_number_name_revision(key))
            if work_name is None:
                continue

            for key2, value2 in self.contents_of_saved_ready_dir.items():
                saved_work_date, saved_work_number, saved_work_name, saved_work_revision = (
                    self._split_folder_name_into_date_number_name_revision(key2))
                if saved_work_name is None:
                    continue

                # if the folder is in saved work
                if work_name == saved_work_name and work_number == saved_work_number:
                    not_found = False
                    # check if the date is newer
                    if work_date > saved_work_date:
                        self.new_folders_in_ready_compared_to_saved_ready[key] = value
                        break
                    # check if the date is older
                    elif work_date < saved_work_date:
                        continue

                    # check if the revision is higher
                    if work_revision > saved_work_revision:
                        self.new_folders_in_ready_compared_to_saved_ready[key] = value
                        break
                    else:
                        continue

            # if the folder is not in saved work, add it to new folders in work
            if not_found:
                self.new_folders_in_ready_compared_to_saved_ready[key] = value

        # correct new_folders_in_work if there is a newer rev in the work dir
        keys_to_remove = []
        for key, value in self.new_folders_in_ready_compared_to_saved_ready.items():
            if key in self.contents_of_saved_ready_dir:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.new_folders_in_ready_compared_to_saved_ready[key]

        # print new folders in work
        print(f"Разлика с предходното състояние на Ready: {self.new_folders_in_ready_compared_to_saved_ready}")

        # prepare the info about new folder to return
        if len(self.new_folders_in_ready_compared_to_saved_ready) > 0:
            info = f"Бр. папки в Ready спрямо предходното състояние: {len(self.new_folders_in_ready_compared_to_saved_ready)}\n"
            count = 1
            for key, value in self.new_folders_in_ready_compared_to_saved_ready.items():
                folder_name = self._extract_text_after_last_backslash(key)
                info += f"{count}) {folder_name}\n"
                count += 1
        else:
            info = None

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.new_folders_in_ready_compared_to_saved_ready)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', None

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported new folders in ready to txt file (see above)')
        return 'Success', info

    # ----------------------------------------------------------------------------------------
    # Finishers
    # ----------------------------------------------------------------------------------------
    # ToDo: where to use it in the process flow?
    def function11_store_current_condition_in_database(self):
        try:
            self.db_controller.delete_all_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        for key, value in self.dict_contents_of_ready_dir.items():
            self.db_controller.insert_data(self.previous_state_table_name, 'dir_path', 'file_names', key, str(value))

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully stored current condition in database')

        return 'Success'

    # ----------------------------------------------------------------------------------------
    # Testing
    # ----------------------------------------------------------------------------------------
    @staticmethod
    def _extract_revision(filename):
        parts = filename.split('_')
        revision = parts[1]
        return revision

    @staticmethod
    def _extract_file_name(filename):
        parts = filename.split('_')
        file_name = parts[0]
        return file_name

    @staticmethod
    def _archive_file(file_path, archive_folder):
        # Create an archive of the file
        file_name = os.path.basename(file_path)
        archive_name = os.path.splitext(file_name)[0] + ".zip"
        archive_path = os.path.join(archive_folder, archive_name)

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, os.path.basename(file_path))

    def function12_testing_of_doc_sorter(self, dir1, dir2, archive_folder):
        try:
            files_list1 = os.listdir(dir1)
            files_list2 = os.listdir(dir2)

            # ToDo: not working since they are now directories not files
            print(os.path.splitext(files_list1[0])[0])
            print(os.path.splitext(files_list2[0])[0])

            for file1 in files_list1:
                for file2 in files_list2:
                    file1_filename = self._extract_file_name(file1)
                    file2_filename = self._extract_file_name(file2)

                    if file1_filename == file2_filename:
                        file1_revision = self._extract_revision(file1)
                        file2_revision = self._extract_revision(file2)

                        if file1_revision > file2_revision:
                            file1_path = os.path.join(dir1, file1)
                            file2_path = os.path.join(dir2, file2)

                            print(f"Replacing {file2} with {file1}")

                            # Archive file2
                            self._archive_file(file2_path, archive_folder)
                            # Remove file2
                            os.remove(file2_path)
                            # Copy file1
                            shutil.copy(file1_path, os.path.join(dir2, file1))

        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully replaced files')
        return 'Success'

    # ToDo: not used
    def function13_read_from_pdf(self, pdf_scanning_coordinates):
        file_path = r'C:\Users\User\Desktop\MK\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28-09-2023-A1.pdf'

        # split pdf_scanning_coordinates
        project_name_coordinates, project_description_coordinates, document_number_coordinates = (
            self._split_pdf_scanning_coordinates(pdf_scanning_coordinates))

        # scan project name
        project_name = extract_text_from_pdf(file_path, project_name_coordinates)
        print(f"Project Name: {project_name}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Project Name: {project_name}")

        # scan project description
        project_description = extract_text_from_pdf(file_path, project_name_coordinates)
        print(f"Project Description: {project_description}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Project Description: {project_description}")

        # scan document number
        document_number = extract_text_from_pdf(file_path, project_name_coordinates)
        print(f"Document Number: {document_number}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Document Number: {document_number}")

        return 'Success'
