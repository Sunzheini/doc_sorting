import re

# -*- coding: utf-8 -*-
from support.constants import folder_regex, file_regex, folder_regex_name_into_number


def extract_text_after_last_backslash(path):
    """
    extracts the text after the last backslash
    :param path: a path with backslashes
    :return: the text after the last backslash
    """
    # Use a regular expression to extract the text after the last backslash
    pattern = r'[^\\]+$'
    match = re.search(pattern, path)
    name = match.group(0)
    return name


def split_folder_name_into_date_number_name_revision(string):
    """
    Splits a folder name into date, number, name and revision
    :param string: folder name
    :return: date, number, name and revision
    """
    pattern = folder_regex
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


def split_file_name_into_number_name_date(string):
    """
    Splits a file name into number and name and date
    :param string: file name
    :return: number and name and date
    """
    pattern = file_regex
    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
        name = match.group(8)
        date = match.group(10)

        return number, name, date
    else:
        return None, None, None


def split_folder_name_into_number(string):
    """
    Splits a folder name into number
    :param string: folder name
    :return: number
    """
    pattern = folder_regex_name_into_number
    match = re.search(pattern, string)

    if match:
        number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)

        return number
    else:
        return None
