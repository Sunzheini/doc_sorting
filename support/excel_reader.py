from openpyxl import load_workbook


file_path = r'C:\Users\User\Desktop\DRAWING_LIST_T317-900-01_for_Daniel.xlsx'


def read_from_excel_file(file_path):
    workbook = load_workbook(file_path)
    # worksheet = workbook[worksheet_name]
    worksheet = workbook[workbook.sheetnames[0]]
    new_dict = {}
    next_line = 0

    for row in worksheet.iter_rows(min_row=4, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
        line_number = row[0].value
        drawing_number = row[1].value
        drawing_name = row[2].value

        new_dict[str(next_line)] = {
            'line_number': line_number,
            'drawing_number': drawing_number,
            'drawing_name': drawing_name
        }
        next_line += 1

    to_print_in_lines = []
    for key, value in new_dict.items():
        to_print_in_lines.append(f'{key}: {value}')

    print(*to_print_in_lines, sep='\n')


read_from_excel_file(file_path)
