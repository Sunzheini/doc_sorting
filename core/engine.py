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
        self.module = ModuleController(
            location_of_log_file, db_controller, paths_table_name, previous_state_table_name, pdf_scanning_coordinates
        )

    def functions_bound_to_button1(self, file_path, work_dir, ready_dir):
        has_additional_message = False
        additional_message = ""

        # ------------------------------------------------------------------------------
        # Scanners
        # ------------------------------------------------------------------------------
        # read from Excel file
        result = self.module.function1_scan_excel(file_path)
        if result != 'Success':
            return result, 'red', None

        # scan work directory
        result = self.module.function2_scan_work_dir(work_dir)
        if result != 'Success':
            return result, 'red', None

        # scan ready directory
        result = self.module.function3_scan_ready_dir(ready_dir)
        if result != 'Success':
            return result, 'red', None

        # extract content of work directory from database
        result = self.module.function4_extract_content_of_work_dir_from_database()
        if result != 'Success':
            return result, 'red', None

        # ------------------------------------------------------------------------------
        # Comparators
        # ------------------------------------------------------------------------------
        # compare work and saved_work directories and provides a dictionary with the differences
        result, temp_message = self.module.function5_new_folders_in_work_compared_to_saved_work()
        if temp_message is not None:
            has_additional_message = True
            additional_message += temp_message
        if result != 'Success':
            return result, 'red', None

        # compare work and ready directories and provides a dictionary with the differences
        result, temp_message = self.module.function6_new_folders_in_work_compared_to_ready()
        if temp_message is not None:
            has_additional_message = True
            additional_message += '\n'
            additional_message += temp_message
        if result != 'Success':
            return result, 'red', None

        # check if new folders in work correspond to Excel file
        result, temp_message = self.module.function7_check_if_new_folders_in_work_and_their_contents_correspond_to_excel()
        if temp_message is not None:
            has_additional_message = True
            additional_message += '\n'
            additional_message += temp_message
        if result != 'Success':
            return result, 'red', None

        # ------------------------------------------------------------------------------
        # Finishers
        # ------------------------------------------------------------------------------
        # store current condition in database
        result = self.module.function11_store_current_condition_in_database()
        if result != 'Success':
            return result, 'red', None

        # return if ok
        if not has_additional_message:
            return 'Сканирането премина успешно', 'green', None
        else:
            return 'Сканирането премина успешно', 'green', additional_message

    def functions_bound_to_button2(self, source_folder, destination_folder, archive_folder):
        has_additional_message = False

        # ----------------------------------------------------------------------------------------
        # Moving
        # ----------------------------------------------------------------------------------------
        additional_message = ""
        result = self.module.function8_move_new_folders_from_work_to_ready(source_folder, destination_folder, archive_folder)
        if result != 'Success':
            return result, 'red', None

        # ----------------------------------------------------------------------------------------
        # Testing
        # ----------------------------------------------------------------------------------------
        # additional_message = ""

        # result = self.module.function12_testing_of_doc_sorter(
        #     source_folder,
        #     destination_folder,
        #     archive_folder,
        # )
        # if result != 'Success':
        #     return result, 'red', None
        #
        # result2 = self.module.function13_read_from_pdf(self.pdf_scanning_coordinates)
        # if result2 != 'Success':
        #     return result2, 'red', None

        if not has_additional_message:
            return 'Обновяването премина успешно', 'green', None
        else:
            return 'Обновяването премина успешно', 'green', additional_message
