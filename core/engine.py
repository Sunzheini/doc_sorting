from core.module_controller import ModuleController


class Engine:
    def __init__(self, location_of_log_file, pdf_scanning_coordinates):
        # locations
        self.location_of_log_file = location_of_log_file
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        # initialize all modules here
        self.module = ModuleController(location_of_log_file)

    # ------------------ module0 ------------------
    def functions_bound_to_button1(self, file_path, work_dir, ready_dir):
        # read from Excel file
        result = self.module.function1_scan_excel(file_path)
        if result != 'Success':
            return result, 'red'

        # scan work directory
        result = self.module.function2_scan_work_dir(work_dir)
        if result != 'Success':
            return result, 'red'

        # scan ready directory
        result = self.module.function3_scan_ready_dir(ready_dir)
        if result != 'Success':
            return result, 'red'

        return 'Сканирането премина успешно', 'green'

    def functions_bound_to_button2(self, source_folder, destination_folder, archive_folder):
        result = self.module.function4_testing_of_doc_sorter(
            source_folder,
            destination_folder,
            archive_folder,
        )
        if result != 'Success':
            return result, 'red'

        result2 = self.module.read_from_pdf(self.pdf_scanning_coordinates)
        if result2 != 'Success':
            return result2, 'red'

        return 'Папките са обновени успешно', 'green'
