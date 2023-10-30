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


# In Python 3.7 and later, dictionaries maintain the insertion order of their items.
def the_walk_loop(directory):
    result_dictionary = {}
    for (dir_path, dir_names, file_names) in walk(directory):
        normalized_path = os.path.normpath(dir_path)
        result_dictionary[normalized_path] = file_names

    # Print in the console for checking
    # for key, value in result_dictionary.items():
    #     print(f'{key}: {value}')

    return result_dictionary
