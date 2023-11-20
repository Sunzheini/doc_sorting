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
    workbook = load_workbook(file_path)
    # worksheet = workbook[worksheet_name]
    worksheet = workbook[workbook.sheetnames[0]]
    new_dict = {}
    next_line = ''
    next_line_number = 0

    # determine start row
    start_row = _determine_start_row_by_given_string(worksheet, string_for_start_row)
    if not start_row:
        return 'Error: Could not find the start row', None

    # reading
    for row in worksheet.iter_rows(min_row=start_row, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
        line_number = row[0].value
        drawing_number = row[1].value
        drawing_name = row[2].value

        # ignore without line_number
        if not line_number:
            continue

        # check if it is a next_line
        if line_number and not drawing_number and drawing_name:
            next_line = str(line_number) + ' ' + drawing_name
            next_line_number = 0
            # print(next_line)
            continue

        temp_new_line = next_line + ' ' + str(next_line_number)

        # if not a next_line, add to the dictionary
        new_dict[temp_new_line] = {
            'line_number': line_number,
            'drawing_number': drawing_number,
            'drawing_name': drawing_name
        }
        # print(new_dict[temp_new_line])
        next_line_number += 1

    # printing in console for checking
    # to_print_in_lines = []
    # for key, value in new_dict.items():
    #     to_print_in_lines.append(f'{key}: {value}')
    # print(*to_print_in_lines, sep='\n')

    # returning the dictionary
    return new_dict
