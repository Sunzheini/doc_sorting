from core.module_controller import ModuleController


class Engine:
    def __init__(
            self,
            location_of_log_file,
            pdf_scanning_coordinates,
            db_controller,
            paths_table_name,
            previous_state_table_name,
    ):
        # locations
        self.location_of_log_file = location_of_log_file
        self.pdf_scanning_coordinates = pdf_scanning_coordinates

        # database
        self.db_controller = db_controller
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name

        # initialize all modules here
        self.module = ModuleController(location_of_log_file, db_controller, paths_table_name, previous_state_table_name)

    # ------------------ module0 ------------------
    def functions_bound_to_button1(self, file_path, work_dir, ready_dir):
        has_additional_message = False

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

        # f4
        result = self.module.function4_extract_content_of_work_dir_from_database()
        if result != 'Success':
            return result, 'red'

        # f5
        result, files = self.module.function5(ready_dir)
        if files is not None:
            has_additional_message = True

        if result != 'Success':
            return result, 'red'

        # store current condition in database
        result = self.module.function6_store_current_condition_in_database()
        if result != 'Success':
            return result, 'red'

        if not has_additional_message:
            return 'Сканирането премина успешно', 'green', None
        else:
            return 'Сканирането премина успешно\n', 'green', files

    def functions_bound_to_button2(self, source_folder, destination_folder, archive_folder):
        result = self.module.function7_testing_of_doc_sorter(
            source_folder,
            destination_folder,
            archive_folder,
        )
        if result != 'Success':
            return result, 'red'

        result2 = self.module.function8_read_from_pdf(self.pdf_scanning_coordinates)
        if result2 != 'Success':
            return result2, 'red'

        return 'Папките са обновени успешно', 'green'
