# -*- coding: windows-1251 -*-
from openpyxl import Workbook


def write_to_excel_file(file_path, data):
    workbook = Workbook()
    worksheet = workbook.active

    for row in data:
        worksheet.append(row)

    workbook.save(file_path)
    return f'Successfully exported to excel file in {file_path}'
