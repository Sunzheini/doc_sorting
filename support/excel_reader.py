# -*- coding: windows-1251 -*-
from openpyxl import load_workbook


def _determine_start_row_by_given_string(worksheet, string_for_start_row):
    start_row = 0
    for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
        for cell in row:
            if cell.value == string_for_start_row:
                start_row = cell.row
                break
        if start_row:
            break
    return start_row


def read_from_excel_file(file_path, string_for_start_row):
    """
    Reads from an Excel file and returns dictionaries by section and by file
    :param file_path:
    :param string_for_start_row:
    :return:
    dict2 {'A Drawings': {'file number file name': {'line number': 'A1.1', 'file number': 'M077-021-001', 'file name': 'Hull...''}}}
    dict3 {'file number file name': {'section number': 'A Drawings', 'line number': 'A1.1'}}
    """
    workbook = load_workbook(file_path)
    worksheet = workbook[workbook.sheetnames[0]]
    dict_by_section = {}
    dict_by_file = {}

    # determine start row
    start_row = _determine_start_row_by_given_string(worksheet, string_for_start_row)
    if not start_row:
        return 'Error: Could not find the start row', None

    # reading
    for row in worksheet.iter_rows(min_row=start_row, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
        line_number = row[0].value      # A.1 or A
        drawing_number = row[1].value   # M077-021-001 or None
        drawing_name = row[2].value     # Hull... or DRAWINGS

        # ignore without line_number
        if not line_number:
            continue

        # check if it is a section
        if line_number and not drawing_number and drawing_name:
            section_number_space_name = line_number + ' ' + drawing_name
            dict_by_section[section_number_space_name] = {}
            continue

        # check if it is a file
        if line_number and drawing_number and drawing_name:
            section_number = line_number[0]

            section_number_space_name = None
            for key in dict_by_section.keys():
                if section_number == key[0]:
                    section_number_space_name = key
                    break

            dict_by_section[section_number_space_name][drawing_number + ' ' + drawing_name] = {}
            dict_by_section[section_number_space_name][drawing_number + ' ' + drawing_name]['line number'] = line_number
            dict_by_section[section_number_space_name][drawing_number + ' ' + drawing_name]['file number'] = drawing_number
            dict_by_section[section_number_space_name][drawing_number + ' ' + drawing_name]['file name'] = drawing_name

    # generating dict3
    for section_number_space_name in dict_by_section.keys():
        for file_number_space_name in dict_by_section[section_number_space_name].keys():
            dict_by_file[file_number_space_name] = {}
            dict_by_file[file_number_space_name]['section number'] = section_number_space_name
            dict_by_file[file_number_space_name]['line number'] = dict_by_section[section_number_space_name][file_number_space_name]['line number']

    # returning the dictionary
    return dict_by_section, dict_by_file
