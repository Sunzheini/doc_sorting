from core.module_controller import ModuleController


# work pc
# source_folder = r'C:\Appl\Projects\Python\Folders to move\Work'
# destination_folder = r'C:\Appl\Projects\Python\Folders to move\Finished'
# archive_folder = r'C:\Appl\Projects\Python\Folders to move\Finished'

# home pc
source_folder = r'C:\Users\User\Desktop\MK\Work'
destination_folder = r'C:\Users\User\Desktop\MK\Ready'
archive_folder = r'C:\Users\User\Desktop\MK\Ready'

# os.makedirs(archive_folder, exist_ok=True)


class Engine:
    def __init__(self, location_of_log_file):
        # locations
        self.location_of_log_file = location_of_log_file

        # initialize all modules here
        self.module0 = ModuleController(location_of_log_file)

    # ------------------ module0 ------------------
    def functions_bound_to_button1(self, file_path, work_dir, ready_dir):
        # read from Excel file
        result = self.module0.function1_scan_excel(file_path)
        if result != 'Success':
            return result, 'red'

        # scan work directory
        result = self.module0.function2_scan_work_dir(work_dir)
        if result != 'Success':
            return result, 'red'

        # scan ready directory
        result = self.module0.function3_scan_ready_dir(ready_dir)
        if result != 'Success':
            return result, 'red'

        return 'Сканирането премина успешно', 'green'

    def functions_bound_to_button2(self):
        result = self.module0.function4_testing_of_doc_sorter(
            source_folder,
            destination_folder,
            archive_folder,
        )

        if result != 'Success':
            return result, 'red'

        return 'Папките са обновени успешно', 'green'
