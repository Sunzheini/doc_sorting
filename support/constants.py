# -*- coding: utf-8 -*-
import os


# default_paths (can be changed via the menu) ------------------------------------------------
ready_dir_path = os.path.join('05 DESIGN DOCUMENTS', 'Работна', 'Ready')
finished_dir_path = os.path.join('05 DESIGN DOCUMENTS', '020 CLASSIFICATION DRAWINGS')
excel_file_path = os.path.join('05 DESIGN DOCUMENTS', '020 CLASSIFICATION DRAWINGS')

# database constants -------------------------------------------------------------------------
db_name = "zed.db"
paths_table_name = "zed_paths_table"
previous_state_table_name = "zed_previous_state_table"

# dll info ----------------------------------------------------------------------------------
current_script_path = os.path.abspath(__file__)
pycharm_project_folder = os.path.dirname((os.path.dirname(current_script_path)))
location_of_dll = os.path.join(pycharm_project_folder, "dotnet", "FolderAndFileManipulation", "FolderAndFileManipulation", "bin", "Debug")
dll_name = "FolderAndFileManipulation"

# other constants ----------------------------------------------------------------------------
allowed_file_extensions = ['.pdf', '.dwg', '.zip', '.doc', '.docx', '.xls', '.xlsx']
location_of_log_file = "log.txt"
pdf_scanning_coordinates = {
    'project_name': {'x1': 2135, 'y1': 1527, 'x2': 2355, 'y2': 1556},
    'project_description': {'x1': 2135, 'y1': 1565, 'x2': 2355, 'y2': 1598},
    'document_number': {'x1': 2135, 'y1': 1608, 'x2': 2310, 'y2': 1640},
}
content_of_excel_file_start_row = 'A'

# regex patterns -----------------------------------------------------------------------------
# folder_regex = r'(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(?:\s*-\s*|\s*-|\s*-|-\s*)?((\d)?)'
# ToDo: 01.05.2024 added to include ( and & and - in the folder name
folder_regex = r'(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-zА-Яа-я]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-zА-Яа-я\.\(\)\,\&\-\s]+(?=\S)[A-Za-zА-Яа-я\)\s])(?:\s*-\s*|\s*-|\s*-|-\s*)?((\d)?)'

file_regex = r'([A-Za-zА-Яа-я]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-zА-Яа-я\s]+(?=\S)[A-Za-zА-Яа-я\s])(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'
# ToDo: 1. Added this one:
file_regex_new_format = r'([A-Za-zА-Яа-я]+)(\d+)(\s*[-_]\s*|\s*-\s*|[-_]\s*|-\s*)(\d+)(\s*[-_]\s*|\s*-\s*|[-_]\s*|-\s*)(\d+)(\s*[-_]\s*|\s*-\s*|[-_]\s*|-\s*)(\d+)'

folder_regex_name_into_number = r'([A-Za-zА-Яа-я]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'
# folder_regex_name_into_number_name = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])'
# ToDo: 01.05.2024 added to include ( and & and - in the folder name
folder_regex_name_into_number_name = r'([A-Za-zА-Яа-я]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-zА-Яа-я\(\)\&\s]+(?=\S)[A-Za-zА-Яа-я\)\s])'

# ToDo: changed here
# ------------------------------------------------------------------------------------------------
rates = {
    'Lto': 25,
    'BoH': 18,
    'VYA': 18,
    'Nve': 20,
    'NiV': 19,
    'AIA': 14,
    'BoM': 22,

    'Pon': 50,
    'PM': 40,
    'Akhn': 60,
    'Cha': 30,
}
location_of_json_file = "opened_projects.json"
location_of_statistics_file = "statistics.xlsx"
