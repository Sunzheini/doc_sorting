import random
import os
import shutil
import zipfile
import re

from pdf_module.pdf_reader import extract_text_from_pdf
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
    ):
        self.location_of_log_file = location_of_log_file

        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name

        self.contents_of_file = None
        self.contents_of_work_dir = None
        self.contents_of_ready_dir = None

        self.contents_of_saved_work_dir = None

    # ----------------------------------------------------------------------------------------
    # Internal
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

    @staticmethod
    def _split_pdf_scanning_coordinates(pdf_scanning_coordinates):
        project_name_coordinates = pdf_scanning_coordinates['project_name']
        project_description_coordinates = pdf_scanning_coordinates['project_description']
        document_number_coordinates = pdf_scanning_coordinates['document_number']

        return project_name_coordinates, project_description_coordinates, document_number_coordinates

    # ----------------------------------------------------------------------------------------
    # External
    # ----------------------------------------------------------------------------------------
    def function1_scan_excel(self, file_path):
        # read from Excel file
        try:
            self.contents_of_file = read_from_excel_file(file_path)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # export to txt file
        try:
            append_a_dict_to_txt_file(self.location_of_log_file, self.contents_of_file)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported excel to txt file')

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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported work dir to txt file')

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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported ready dir to txt file')

        return 'Success'

    def function4_extract_content_of_work_dir_from_database(self):
        # Retrieve data from the database
        try:
            data = self.db_controller.retrieve_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        # Extract the data
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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported saved work dir to txt file')

        return 'Success'

    # ToDo: how to compare and by which criteria to compare
    def function5(self, ready_dir):
        # prints contents of the 3 sources
        print(f"Now in work: {self.contents_of_work_dir}")
        print(f"Now in ready: {self.contents_of_ready_dir}")
        print(f"Saved work: {self.contents_of_saved_work_dir}")

        # check for new folders in work compared to saved work
        new_folders_in_work = {}
        for key, value in self.contents_of_work_dir.items():
            if key not in self.contents_of_saved_work_dir.keys():
                new_folders_in_work[key] = value

        # print new folders in work
        print(f"New folders in work: {new_folders_in_work}")

        # prepare the info about new folder to return
        if len(new_folders_in_work) > 0:
            info = f"Number of new folders in work: {len(new_folders_in_work)}\n"
            count = 1
            for key, value in new_folders_in_work.items():
                path = key
                # Use a regular expression to extract the text after the last backslash
                pattern = r'[^\\]+$'
                match = re.search(pattern, path)
                folder_name = match.group(0)
                info += f"{count}) {folder_name}\n"
                count += 1
        else:
            info = None

        return 'Success', info

    def function6_store_current_condition_in_database(self):
        try:
            self.db_controller.delete_all_data(self.previous_state_table_name)
        except Exception as e:
            append_a_string_to_txt_file(self.location_of_log_file, f'Error: {e}')
            return f'Error: {e}'

        for key, value in self.contents_of_work_dir.items():
            self.db_controller.insert_data(self.previous_state_table_name, 'dir_path', 'file_names', key, str(value))

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully stored current condition in database')

        return 'Success'

    def function7_testing_of_doc_sorter(self, dir1, dir2, archive_folder):
        try:
            files_list1 = os.listdir(dir1)
            files_list2 = os.listdir(dir2)

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

    def function8_read_from_pdf(self, pdf_scanning_coordinates):
        # split pdf_scanning_coordinates
        project_name_coordinates, project_description_coordinates, document_number_coordinates = (
            self._split_pdf_scanning_coordinates(pdf_scanning_coordinates))

        # project name
        project_name = extract_text_from_pdf(project_name_coordinates)
        print(f"Project Name: {project_name}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Project Name: {project_name}")

        # project description
        project_description = extract_text_from_pdf(project_description_coordinates)
        print(f"Project Description: {project_description}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Project Description: {project_description}")

        # document number
        document_number = extract_text_from_pdf(document_number_coordinates)
        print(f"Document Number: {document_number}")
        append_a_string_to_txt_file(self.location_of_log_file, f"Document Number: {document_number}")

        return 'Success'
