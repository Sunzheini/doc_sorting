import os
from os import walk


def check_if_file_name_contains_text(file_path, text):
    if text in os.path.basename(file_path):
        return True
    return False


def get_list_of_all_files_of_type_in_a_dir(directory, file_ending):
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_ending):
                result.append(os.path.join(root, file))
    return result


def search_keyword_in_all_files_in_a_dir(directory, keyword):
    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_number, line in enumerate(f, 1):
                        if keyword in line:
                            result = {
                                'file_path': file_path,
                                'line_number': line_number,
                                'line_content': line.strip()
                            }
                            results.append(result)
    return results


def the_walk_loop(directory):
    for (dir_path, dir_names, file_names) in walk(directory):
        pass

        for directory in dir_names:
            pass

        for file in file_names:
            pass
