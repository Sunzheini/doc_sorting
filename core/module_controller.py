# -*- coding: windows-1251 -*-

import os
import shutil
import zipfile
import re

from support.pdf_reader import extract_text_from_pdf
from support.excel_reader import read_from_excel_file
from support.get_info import the_walk_loop
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

        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        self.contents_of_file = None
        self.contents_of_work_dir = None
        self.contents_of_ready_dir = None
        self.contents_of_saved_work_dir = None

        self.new_folders_in_work_compared_to_saved_work = None
        self.new_folders_in_work_compared_to_ready = None

    # ----------------------------------------------------------------------------------------
    # Scanners
    # ----------------------------------------------------------------------------------------
    def function1_scan_excel(self, file_path):
        # read from Excel file
        try:
            self.contents_of_file = read_from_excel_file(file_path)
            print(f"Contents of file: {self.contents_of_file}")
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_file)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported excel to txt file (see above)')
        return 'Success'

    def function2_scan_work_dir(self, work_dir):
        # scan work directory
        try:
            self.contents_of_work_dir = the_walk_loop(work_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_work_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported work dir to txt file (see above)')
        return 'Success'

    def function3_scan_ready_dir(self, ready_dir):
        # scan ready directory
        try:
            self.contents_of_ready_dir = the_walk_loop(ready_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_ready_dir)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported ready dir to txt file (see above)')
        return 'Success'

    def function4_extract_content_of_work_dir_from_database(self):
        # Retrieve data from the database
        try:
            data = self.db_controller.retrieve_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # Fill the dictionary with the retrieved data
        try:
            self.contents_of_saved_work_dir = {}
            for row in data:
                self.contents_of_saved_work_dir[row[1]] = row[2]
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_saved_work_dir)
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
    def _print_current_contents_of_the_3_folders(self):
        print(f"Now in Work: {self.contents_of_work_dir}")
        print(f"Now in Ready: {self.contents_of_ready_dir}")
        print(f"Now in Saved work: {self.contents_of_saved_work_dir}")

    @staticmethod
    def _split_folder_name_into_date_name_revision(string):
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
    def _split_file_name_into_number_name_revision(string):
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

    # ToDo: currently this is working by adding the folders 1 by 1 from source to work_dir and clicking the button1
    def function5_new_folders_in_work_compared_to_saved_work(self):
        # prints contents of the 3 sources
        self._print_current_contents_of_the_3_folders()

        self.new_folders_in_work_compared_to_saved_work = {}
        for key, value in self.contents_of_work_dir.items():
            not_found = True
            work_date, work_number, work_name, work_revision = (
                self._split_folder_name_into_date_name_revision(key))
            if work_name is None:
                continue

            for key2, value2 in self.contents_of_saved_work_dir.items():
                saved_work_date, saved_work_number, saved_work_name, saved_work_revision = (
                    self._split_folder_name_into_date_name_revision(key2))
                if saved_work_name is None:
                    continue

                # if the folder is in saved work
                if work_name == saved_work_name and work_number == saved_work_number:
                    not_found = False
                    # check if the date is newer
                    if work_date > saved_work_date:
                        self.new_folders_in_work_compared_to_saved_work[key] = value
                        break
                    # check if the date is older
                    elif work_date < saved_work_date:
                        continue

                    # check if the revision is higher
                    if work_revision > saved_work_revision:
                        self.new_folders_in_work_compared_to_saved_work[key] = value
                        break
                    else:
                        continue

            # if the folder is not in saved work, add it to new folders in work
            if not_found:
                self.new_folders_in_work_compared_to_saved_work[key] = value

        # correct new_folders_in_work if there is a newer rev in the work dir
        keys_to_remove = []
        for key, value in self.new_folders_in_work_compared_to_saved_work.items():
            if key in self.contents_of_saved_work_dir:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.new_folders_in_work_compared_to_saved_work[key]

        # print new folders in work
        print(f"Разлика с предходното състояние на Work: {self.new_folders_in_work_compared_to_saved_work}")

        # prepare the info about new folder to return
        if len(self.new_folders_in_work_compared_to_saved_work) > 0:
            info = f"Бр. папки в Work спрямо предходното състояние: {len(self.new_folders_in_work_compared_to_saved_work)}\n"
            count = 1
            for key, value in self.new_folders_in_work_compared_to_saved_work.items():
                folder_name = self._extract_text_after_last_backslash(key)
                info += f"{count}) {folder_name}\n"
                count += 1
        else:
            info = None

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.new_folders_in_work_compared_to_saved_work)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', None

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported new folders in work to txt file (see above)')
        return 'Success', info

    def function6_new_folders_in_work_compared_to_ready(self):
        self.new_folders_in_work_compared_to_ready = {}
        for key, value in self.contents_of_work_dir.items():
            not_found = True
            work_date, work_number, work_name, work_revision = (
                self._split_folder_name_into_date_name_revision(key))
            if work_name is None:
                continue

            for key2, value2 in self.contents_of_ready_dir.items():
                ready_date, ready_number, ready_name, ready_revision = (
                    self._split_folder_name_into_date_name_revision(key2))
                if ready_name is None:
                    continue

                # if the folder is in ready
                if work_name == ready_name and work_number == ready_number:
                    not_found = False
                    # check if the date is newer
                    if work_date > ready_date:
                        self.new_folders_in_work_compared_to_ready[key] = value
                        break
                    # check if the date is older
                    elif work_date < ready_date:
                        continue

                    # check if the revision is higher
                    if work_revision > ready_revision:
                        self.new_folders_in_work_compared_to_ready[key] = value
                        break
                    else:
                        continue

            # if the folder is not in ready, add it to new folders in work
            if not_found:
                self.new_folders_in_work_compared_to_ready[key] = value

        # correct new_folders_in_work if there is a newer rev in the work dir
        keys_to_remove = []
        for key, value in self.new_folders_in_work_compared_to_ready.items():
            if key in self.contents_of_ready_dir:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.new_folders_in_work_compared_to_ready[key]

        # print new folders in work
        print(f"Разлика между Work и Ready: {self.new_folders_in_work_compared_to_ready}")

        # prepare the info about new folder to return
        if len(self.new_folders_in_work_compared_to_ready) > 0:
            info = f"Бр. нови папки в Work спрямо Ready: {len(self.new_folders_in_work_compared_to_ready)}\n"
            count = 1
            for key, value in self.new_folders_in_work_compared_to_ready.items():
                folder_name = self._extract_text_after_last_backslash(key)
                info += f"{count}) {folder_name}\n"
                count += 1
        else:
            info = None

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.new_folders_in_work_compared_to_ready)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return 'Error', None

        # return
        append_a_string_to_txt_file(self.location_of_log_file,
                                    'Successfully exported new folders in work to txt file (see above)')
        return 'Success', info

    def function7_check_if_new_folders_in_work_and_their_contents_correspond_to_excel(self):
        return_info = ""
        count = 1

        # check if the new folders in work correspond to Excel file
        for key, value in self.new_folders_in_work_compared_to_ready.items():
            work_date, work_number, work_name, work_revision = (
                self._split_folder_name_into_date_name_revision(key))
            if work_name is None:
                continue

            # check if the folder is in the Excel file
            for key2, value2 in self.contents_of_file.items():
                if self._compare_by_name_and_number(work_name, work_number, value2['drawing_name'], value2['drawing_number']):
                    return_info += f"{count}. Папката {work_name} с номер {work_number} съответства на Excel файла\n"

                    # check the list, which contains the files in the folder
                    for file in value:
                        file_extension = os.path.splitext(file)[1]
                        file_number, file_name = (
                            self._split_file_name_into_number_name_revision(file))
                        if file_name is None:
                            continue

                        # check if the file is in the Excel file
                        if self._compare_by_name_and_number(file_name, file_number, value2['drawing_name'], value2['drawing_number']):
                            return_info += f"- Файлът {file_name}{file_extension} с номер {file_number} съответства на Excel файла\n"
                        else:
                            return_info += f"- Файлът {file_name}{file_extension} с номер {file_number} НЕ съответства на Excel файла\n"

                        # scan pdf files and check if they correspond to Excel file
                        if file_extension == '.pdf':
                            file_path = os.path.join(key, file)

                            project_name, project_description, document_number = (
                                self._scan_pdf(file_path, self.pdf_scanning_coordinates))
                            return_info += f"--- Номер на документ: {document_number}\n"
                            return_info += f"--- Описание на проект: {project_description}\n"
                            return_info += f"--- Име на проект: {project_name}\n"

                            if self._compare_by_name_and_number(project_name, document_number, value2['drawing_name'], value2['drawing_number']):
                                return_info += f"--- Съответства на Excel файла\n"
                            else:
                                return_info += f"--- НЕ съответства на Excel файла\n"

                    break
            else:
                return_info += f"{count}. Папката {work_name} с номер {work_number} НЕ съответства на Excel файла\n"

            count += 1

        # export to txt file
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
    # Finishers
    # ----------------------------------------------------------------------------------------
    # ToDo: where to use it in the process flow?
    def function11_store_current_condition_in_database(self):
        try:
            self.db_controller.delete_all_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        for key, value in self.contents_of_work_dir.items():
            self.db_controller.insert_data(self.previous_state_table_name, 'dir_path', 'file_names', key, str(value))

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully stored current condition in database')

        return 'Success'

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

    def function8_move_new_folders_from_work_to_ready(self, source_folder, destination_folder, archive_folder):
        for key, value in self.new_folders_in_work_compared_to_ready.items():
            work_folder_date, work_folder_number, work_folder_name, work_folder_revision = (
                self._split_folder_name_into_date_name_revision(key))

            # find the folders to archive
            for folder in self.contents_of_ready_dir:
                ready_folder_date, ready_folder_number, ready_folder_name, ready_folder_revision = (
                    self._split_folder_name_into_date_name_revision(folder))

                # if the folder is in ready, archive it and remove it
                if ready_folder_name == work_folder_name and ready_folder_number == work_folder_number:
                    self._archive_folder(folder, archive_folder)
                    shutil.rmtree(folder)

            # move the folder
            shutil.move(key, destination_folder)

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
