# -*- coding: utf-8 -*-
import os


def replace_lower_dashes_with_spaces(string):
    """
    replaces lower dashes with spaces
    :param string: string to be processed
    :return: string with spaces instead of lower dashes
    """
    return string.replace("_", " ")


def normalize_path_to_have_only_forward_slashes(string):
    """
    normalizes a path to have only forward slashes
    :param string:
    :return: path with only forward slashes
    """
    result = os.path.normpath(string)
    return result
