from core.module_controller import ModuleController


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
        pass
