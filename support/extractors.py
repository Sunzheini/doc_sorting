import re

# -*- coding: utf-8 -*-
from support.constants import folder_regex, file_regex, folder_regex_name_into_number, \
    folder_regex_name_into_number_name, file_regex_new_format


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


def split_string_24072025(s):
    # Match DATE (digits), then first delimiter, then CODE (all until last delimiter), then DESCRIPTION
    match = re.match(r'^(\d+)[-_](.*?)[-_]([^-_]*)$', s)
    if not match:
        # Alternative pattern if DESCRIPTION contains delimiters (e.g., "Ladder-VL3")
        match = re.match(r'^(\d+)[-_](.*)[-_](.*)$', s)
    if match:
        date_part, code_part, desc_part = match.groups()
        # Remove trailing delimiters
        code_part = code_part.rstrip('-_')
        desc_part = desc_part.rstrip('-_')
        return date_part, code_part, desc_part
    return None  # Fallback if no match


def split_folder_name_into_date_number_name_revision(string):
    """
    Splits a folder name into date, number, name and revision
    :param string: folder name
    :return: date, number, name and revision
    """
    # pattern = folder_regex
    # match = re.search(pattern, string)
    #
    # if match:
    #     date = match.group(1)
    #     number = match.group(3) + match.group(4) + '-' + match.group(6) + '-' + match.group(8)
    #     name = match.group(10)
    #     revision = match.group(11)
    #
    #     if revision == "":
    #         revision = 0
    #
    #     return date, number, name, revision
    # else:
    #     return None, None, None, None

    split_character: str = '-'

    # split_string = string.split(split_character)
    split_string = split_string_24072025(string)
    date = split_string[0]
    number = split_string[1]
    name = split_string[2]
    revision = 0

    if len(split_string) > 3:
        revision = int(split_string[3])

    return date, number, name, revision


def split_file_name_into_number_name_date(string):
    """
    Splits a file name into number and name and date
    :param string: file name
    :return: number and name and date
    """
    # pattern = file_regex
    # match = re.search(pattern, string)
    #
    # # ToDo: 2. Changed here
    # # if there is no match with the old pattern, try the new one
    # if match:
    #     number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
    #     name = match.group(8)
    #     date = match.group(10)
    #     return number, name, date
    # else:
    #     pattern = file_regex_new_format
    #     match = re.search(pattern, string)
    #
    #     if match:
    #         number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
    #         name = None
    #         date = match.group(8)
    #         return number, name, date
    #
    #     else:
    #         return None, None, None

    split_character = '_'
    split_string = string.split(split_character)
    number = split_string[0]
    name = None
    date = split_string[1]

    #  remove file extension
    date = date.split('.')[0]

    return number, name, date


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


def split_folder_name_into_number_name(string):
    """
    Splits a folder name into number and name
    :param string: folder name
    :return: number and name
    """

    # pattern = folder_regex_name_into_number_name
    # match = re.search(pattern, string)
    #
    # if match:
    #     number = match.group(1) + match.group(2) + '-' + match.group(4) + '-' + match.group(6)
    #     name = match.group(8)
    #
    #     return number, name
    # else:
    #     return None, None

    split_character = '_'
    split_string = string.split(split_character)
    number = split_string[0]

    if len(split_string) > 1:
        name = split_string[1]
    else:
        number = None
        name = None

    return number, name
