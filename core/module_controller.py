import random

from support.excel_reader import read_from_excel_file
from support.get_info import the_walk_loop
from support.txt_writer import append_a_dict_to_txt_file, append_a_string_to_txt_file


class ModuleController:
    def __init__(self, location_of_log_file):
        self.location_of_log_file = location_of_log_file

        self.contents_of_file = None
        self.contents_of_work_dir = None
        self.contents_of_ready_dir = None

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
