import random
import os
import shutil
import zipfile

from support.excel_reader import read_from_excel_file
from support.get_info import the_walk_loop
from support.txt_writer import append_a_dict_to_txt_file, append_a_string_to_txt_file


class ModuleController:
    def __init__(self, location_of_log_file):
        self.location_of_log_file = location_of_log_file

        self.contents_of_file = None
        self.contents_of_work_dir = None
        self.contents_of_ready_dir = None

    # ----------------------------------------------------------------------------------------
    # Internal
    # ----------------------------------------------------------------------------------------
    def _extract_revision(self, filename):
        parts = filename.split('_')
        revision = parts[1]
        return revision

    def _extract_file_name(self, filename):
        parts = filename.split('_')
        file_name = parts[0]
        return file_name

    def _archive_file(self, file_path, archive_folder):
        # Create an archive of the file
        file_name = os.path.basename(file_path)
        archive_name = os.path.splitext(file_name)[0] + ".zip"
        archive_path = os.path.join(archive_folder, archive_name)

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, os.path.basename(file_path))


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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported to txt file')

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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported to txt file')

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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully exported to txt file')

        return 'Success'

    def function4_testing_of_doc_sorter(self, dir1, dir2, archive_folder):
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

        append_a_string_to_txt_file(self.location_of_log_file, 'Successfully tested')

        return 'Success'
