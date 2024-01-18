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

# other constants ----------------------------------------------------------------------------
location_of_log_file = "log.txt"
pdf_scanning_coordinates = {
    'project_name': {'x1': 2135, 'y1': 1527, 'x2': 2355, 'y2': 1556},
    'project_description': {'x1': 2135, 'y1': 1565, 'x2': 2355, 'y2': 1598},
    'document_number': {'x1': 2135, 'y1': 1608, 'x2': 2310, 'y2': 1640},
}

# regex patterns -----------------------------------------------------------------------------
folder_regex = r'(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(?:\s*-\s*|\s*-|\s*-|-\s*)?((\d)?)'
file_regex = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'
folder_regex_name_into_number = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'
