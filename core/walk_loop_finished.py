# -*- coding: utf-8 -*-
import os
from os import walk

from support.extractors import extract_text_after_last_backslash, split_folder_name_into_number, \
    split_file_name_into_number_name_date, split_folder_name_into_number_name
from support.formatters import normalize_path_to_have_only_forward_slashes


def the_walk_loop_finished(directory):
    """
    In Python 3.7 and later, dictionaries maintain the insertion order of their items!

    walks recursively through a directory, returns a 3-tuple (dir_path, dir_names, file_names)
        - dir_path: the path to the dir C:/Users/User/Desktop/MK/ProjectXYZ\05 DESIGN DOCUMENTS\Работна\Ready
        - dir_names: the names of the subdirs in dir_path ['20230928 - MC077...', ]
        - file_names: the names of the files in dir_path ['20230928 - MC077...', ]

    :param directory containing
        - subdirs: 20230930 - MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 1
        - and files: MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf

    :return: a dictionary with the following structure:
    {'MC077-021-001 Leak proof joint design and drawing for hull': {
        'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull',
        'files': {
            'MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf': {
                'number': 'MC077-021-001',
                'name': 'Leak proof joint design and drawing for hull',
                'date': '28092023',
                'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023-A1.pdf'},
            'MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg': {
                'number': 'MC077-021-001',
                'name': 'Leak proof joint design and drawing for hull',
                'date': '28092023',
                'path': 'C:\\Users\\User\\Desktop\\MK\\ProjectXYZ\\05 DESIGN DOCUMENTS\\020 CLASSIFICATION DRAWINGS\\A DRAWINGS\\20230928 - MC077-021-001-Leak proof joint design and drawing for hull\\MC077-021-001-Leak proof joint design and drawing for hull - 28092023.dwg'}}},

    Currently: 'MC077-021-001 Leak proof joint design and drawing for hull'
    is:        'MC077-021-001'      because of the error
    """
    result = {}

    # check if the directory exists
    if not os.path.exists(directory):
        return result

    # check if the directory is empty
    if not os.listdir(directory):
        return result

    for (dir_path, dir_names, file_names) in walk(directory):

        # skip if there are subdirs
        if dir_names:
            continue

        dir_path_after_last_backslash = extract_text_after_last_backslash(dir_path)

        # ------------------------------------------------------------------------------
        # this is different in the ready dir

        # ToDo: comment this, since now only creating a folder with a folder number works!
        folder_number, folder_name = split_folder_name_into_number_name(dir_path_after_last_backslash)
        if folder_number is None and folder_name is None:
            continue
        folder_number_space_name = folder_number + ' ' + folder_name

        # ToDo: uncomment this, since now only creating a folder with a folder number works!
        # folder_number = split_folder_name_into_number(dir_path_after_last_backslash)
        # if folder_number is None:
        #     continue
        # folder_number_space_name = folder_number

        # ------------------------------------------------------------------------------
        # checks for higher date and higher revision     # not needed opposite to the ready dir

        # ------------------------------------------------------------------------------
        # add the folder to the result
        result[folder_number_space_name] = {
            # 'date': folder_date,              # there is no date here opposite to the ready dir
            # 'rev': folder_revision,           # there is no revision here opposite to the ready dir
            'path': normalize_path_to_have_only_forward_slashes(dir_path),
            'files': {}
        }

        for file in file_names:
            file_number, file_name, file_date = split_file_name_into_number_name_date(file)

            result[folder_number_space_name]['files'][file] = {
                'number': file_number,
                'name': file_name,
                'date': file_date,
                'path': normalize_path_to_have_only_forward_slashes(os.path.join(dir_path, file))
            }

    return result
