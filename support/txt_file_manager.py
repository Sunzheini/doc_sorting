# -*- coding: utf-8 -*-


def append_a_dict_to_txt_file(path_to_txt, dictionary):
    """
    Appends a dictionary to a txt file
    :param path_to_txt: the path to the txt file
    :param dictionary: the dictionary to be appended
    :return: a message that the dictionary was successfully appended to the txt file
    """
    with open(path_to_txt, 'a', encoding='utf-8', ) as file:
        file.write('\n')
        file.write('\n')
        for key, value in dictionary.items():
            file.write(f'{key}: {value}\n')
    return f'Successfully exported the dict to a txt file in {path_to_txt}'


def append_a_string_to_txt_file(path_to_txt, string):
    """
    Appends a string to a txt file
    :param path_to_txt: the path to the txt file
    :param string: the string to be appended
    :return: a message that the string was successfully appended to the txt file
    """
    with open(path_to_txt, 'a', encoding='utf-8', ) as file:
        file.write('\n')
        file.write(string)
    return f'Successfully exported the string to txt file in {path_to_txt}'
