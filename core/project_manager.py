import json
import os
from openpyxl import Workbook


class ProjectManager:
    def __init__(self, location_of_json_file):
        self.json_file = location_of_json_file
        self.projects = self._load_projects()

    def _load_projects(self):
        """
        Load the projects from the JSON file. If the file does not exist or is empty, return an empty dictionary.
        :return: Dictionary of projects.
        """
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    # In case the file is empty or invalid, return an empty dictionary
                    return {}
        else:
            return {}

    def _save_projects(self):
        """
        Save the projects dictionary to the JSON file.
        """
        with open(self.json_file, 'w') as file:
            json.dump(self.projects, file, indent=4)

    def write_opened_project_into_the_json_file(self, project_name):
        """
        Write the opened project into the json file if it's not already present.
        :param project_name: name of the project.
        """
        if project_name not in self.projects:
            self.projects[project_name] = {}
            self._save_projects()
            print(f"Project '{project_name}' added.")
        else:
            print(f"Project '{project_name}' already exists.")

    # def write_data_into_the_json_file(self, project_dir, data_dictionary):
    #     """
    #     Write the data into the json file for a specific project directory.
    #     :param project_dir: name of the project directory.
    #     :param data_dictionary: data to write.
    #     """
    #     # Ensure the project directory is initialized in the dictionary
    #     if project_dir not in self.projects:
    #         self.projects[project_dir] = {}
    #
    #     # Update the existing dictionary for the project directory
    #     for project_name, details in data_dictionary.items():
    #         self.projects[project_dir][project_name] = details
    #
    #     # Save the updated projects dictionary to the JSON file
    #     self._save_projects()
    #
    #     print(f"Data for project directory '{project_dir}' has been updated in the JSON file.")

    # ToDo: 16.08.2024
    def write_data_into_the_json_file(self, project_dir, data_dictionary):
        """
        Write the data into the json file for a specific project directory.
        :param project_dir: name of the project directory: 'C:/Users/User/Desktop/MK/new/Project160824'
        :param data_dictionary: data to write:
        {'PD069-041-02 Crane foundation SB':
            {'responsible_person': '1', 'price': '2', 'hours': '3', 'date': '2024-08-16'},
         'PD069-022-04 Pulling eyes':
            {'responsible_person': '4', 'price': '5', 'hours': '6', 'date': '2024-08-16'},
         'PD069-022-01 ANCHORING & TOWING EQUIMENT':
            {'responsible_person': '7', 'price': '8', 'hours': '9', 'date': '2024-08-16'}}
        """
        # Ensure the project directory is initialized in the dictionary
        if project_dir not in self.projects:
            self.projects[project_dir] = {}

        # Update the existing dictionary for the project directory
        for project_name, details in data_dictionary.items():

            # Check if the project name is already present in the project directory
            if project_name in self.projects[project_dir]:

            # Get the existing value of `passed`
                passed = self.projects[project_dir][project_name].get('passed', False)
                new_passed = int(passed) + 1
                details['passed'] = str(new_passed)

            else:
                details['passed'] = '1'

            # Update the existing dictionary for the project directory
            self.projects[project_dir][project_name] = details

        # Save the updated projects dictionary to the JSON file
        self._save_projects()

        print(f"Data for project directory '{project_dir}' has been updated in the JSON file.")

    def export_to_excel(self, excel_file_path):
        """
        Export the JSON data to an Excel file using openpyxl.
        :param excel_file_path: Path where the Excel file will be saved.
        """
        # Create a new Workbook and select the active worksheet
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Projects"

        # Prepare headers
        headers = ['Project Directory', 'Project Item']
        first_row = True

        for project_dir, projects in self.projects.items():
            for project_name, details in projects.items():
                if first_row:
                    # Add headers dynamically from the keys in the first project
                    headers.extend(details.keys())
                    sheet.append(headers)
                    first_row = False

                # Prepare the row data
                row = [project_dir, project_name] + [details.get(header, '') for header in headers[2:]]
                sheet.append(row)

        # Save the workbook to the specified file path
        workbook.save(excel_file_path)
        print(f"Data has been exported to '{excel_file_path}'.")
