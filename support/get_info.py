# -*- coding: utf-8 -*-
import os
import re
from os import walk

from support.custom_functions_lib import normalize_path_to_have_only_forward_slashes


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


def split_folder_name_into_date_number_name_revision(string):
    pattern = r'(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(?:\s*-\s*|\s*-|\s*-|-\s*)?((\d)?)'

    match = re.search(pattern, string)

    if match:
        date = match.group(1)
        number = match.group(3) + match.group(4) + '-' + match.group(6) + '-' + match.group(8)
        name = match.group(10)
        revision = match.group(11)

        if revision == "":
            revision = 0

        return date, number, name, revision
    else:
        return None, None, None, None


def split_folder_name_into_number_name(string):
    pattern = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])'

    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
        name = match.group(8)

        return number, name
    else:
        return None, None


def split_file_name_into_number_name(string):
    pattern = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'

    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
        name = match.group(8)

        return number, name
    else:
        return None, None


def split_file_name_into_number_name_date(string):
    pattern = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)([A-Za-z\s]+(?=\S)[A-Za-z\s])(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'

    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
        name = match.group(8)
        date = match.group(10)

        return number, name, date
    else:
        return None, None, None


def split_folder_name_into_number(string):
    pattern = r'([A-Za-z]+)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)(\s*-\s*|\s*-|-\s*|-\s*)(\d+)'

    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)

        return number
    else:
        return None


def extract_text_after_last_backslash(path):
    # Use a regular expression to extract the text after the last backslash
    pattern = r'[^\\]+$'
    match = re.search(pattern, path)
    name = match.group(0)
    return name


# In Python 3.7 and later, dictionaries maintain the insertion order of their items.
def the_walk_loop_ready(directory):
    """
    walks recursively through a directory, returns a 3-tuple (dir_path, dir_names, file_names)
    dir_path: the path to the dir C:/Users/User/Desktop/MK/ProjectXYZ\05 DESIGN DOCUMENTS\Работна\Ready
    dir_names: the names of the subdirs in dir_path ['20230928 - MC077...', ]
    file_names: the names of the files in dir_path ['20230928 - MC077...', ]
    :param directory containing
    subdirs: 20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1
    and files MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf
    :return: a dictionary with the following structure:
    # {'MC077-021-001 Leak proof joint design and drawing for hull': {'date': '20230928', 'rev': 0, 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull', 'files': {'MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf': {'number': 'MC077-021-001', 'name': 'Leak proof joint design and drawing for hull', 'date': '28092023', 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf'}, 'MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg': {'number': 'MC077-021-001', 'name': 'Leak proof joint design and drawing for hull', 'date': '28092023', 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg'}}}, 'MC077-022-001 Leak proof joint design and drawing for tank and deck surface': {'date': '20230928', 'rev': 0, 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface', 'files': {'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023-A1.pdf': {'number': 'MC077-022-001', 'name': 'Leak proof joint design and drawing for tank and deck surface', 'date': '28092023', 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023-A1.pdf'}, 'MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg': {'number': 'MC077-022-001', 'name': 'Leak proof joint design and drawing for tank and deck surface', 'date': '28092023', 'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\Работна\\Ready\\20230928 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface\\MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 28092023.dwg'}}}}
    """
    result = {}

    # check if the directory exists
    if not os.path.exists(directory):
        return result

    # check if the directory is empty
    if not os.listdir(directory):
        return result

    for (dir_path, dir_names, file_names) in walk(directory):
        if dir_names:
            continue

        dir_path_after_last_backslash = extract_text_after_last_backslash(dir_path)
        folder_date, folder_number, folder_name, folder_revision = split_folder_name_into_date_number_name_revision(dir_path_after_last_backslash)
        folder_number_space_name = folder_number + ' ' + folder_name

        # ------------------------------------------------------------------------------
        if folder_number_space_name in result.keys():
            # check if key exists with a higher date
            if int(folder_date) < int(result[folder_number_space_name]['date']):
                continue

            # check if key exists with a higher revision
            if int(folder_revision) < int(result[folder_number_space_name]['rev']):
                continue

        # ------------------------------------------------------------------------------

        result[folder_number_space_name] = {
            'date': folder_date,
            'rev': folder_revision,
            'path': normalize_path_to_have_only_forward_slashes(dir_path),
            'files': {}
        }

        for file in file_names:
            file_number, file_name, file_date = split_file_name_into_number_name_date(file)
            file_number_space_name = file_number + ' ' + file_name

            result[folder_number_space_name]['files'][file] = {
                'number': file_number,
                'name': file_name,
                'date': file_date,
                'path': normalize_path_to_have_only_forward_slashes(os.path.join(dir_path, file))
            }

    return result


def the_walk_loop_finished(directory):
    """
    walks recursively through a directory, returns a 3-tuple (dir_path, dir_names, file_names)
    dir_path: the path to the dir C:/Users/User/Desktop/MK/ProjectXYZ\05 DESIGN DOCUMENTS\Работна\Ready
    dir_names: the names of the subdirs in dir_path ['MC077...', ]
    file_names: the names of the files in dir_path ['20230928 - MC077...', ]
    :param directory containing
    subdirs: MC077-022-001-Leak proof joint design and drawing for tank and deck surface
    and files MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf
    :return: a dictionary with the following structure:
    dict4 {'folder number folder name': {'path': 'C:/Project/Finished/...',
                                          files: {'file name': {'number': 'MC077-021-001', name': 'Leak proof joint design and drawing for hull', 'date': '28092023', 'path': 'C:/Project/Finished/.../MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf'}}}}
    """
    result = {}

    # check if the directory exists
    if not os.path.exists(directory):
        return result

    # check if the directory is empty
    if not os.listdir(directory):
        return result

    for (dir_path, dir_names, file_names) in walk(directory):
        if dir_names:
            continue

        dir_path_after_last_backslash = extract_text_after_last_backslash(dir_path)

        # ToDo: changed this, since now only creating a folder with a folder number works!
        # ------------------------------------------------------------------------------
        # folder_number, folder_name = split_folder_name_into_number_name(dir_path_after_last_backslash)
        #
        # if folder_number is None and folder_name is None:
        #     continue
        #
        # folder_number_space_name = folder_number + ' ' + folder_name

        folder_number = split_folder_name_into_number(dir_path_after_last_backslash)

        if folder_number is None:
            continue

        folder_number_space_name = folder_number

        # ------------------------------------------------------------------------------

        result[folder_number_space_name] = {
            'path': normalize_path_to_have_only_forward_slashes(dir_path),
            'files': {}
        }

        for file in file_names:
            file_number, file_name, file_date = split_file_name_into_number_name_date(file)
            file_number_space_name = file_number + ' ' + file_name

            result[folder_number_space_name]['files'][file] = {
                'number': file_number,
                'name': file_name,
                'date': file_date,
                'path': normalize_path_to_have_only_forward_slashes(os.path.join(dir_path, file))
            }

    return result
