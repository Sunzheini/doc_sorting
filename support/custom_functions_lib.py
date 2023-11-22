# -*- coding: windows-1251 -*-
import os
import time


def replace_lower_dashes_with_spaces(string):
    return string.replace("_", " ")


def normalize_path_to_have_only_forward_slashes(string):
    """
    normalizes a path to have only forward slashes
    :param string:
    :return: path with only forward slashes
    """
    result = os.path.normpath(string)
    return result


def time_measurement_decorator(some_function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = some_function(*args, **kwargs)
        end = time.time()
        measurement = end - start

        # turn to seconds
        if measurement < 0.001:
            measurement *= 1000
            print(f"generated in: {measurement:.3f}ms")
        else:
            print(f"generated in: {measurement:.3f}s")

        return result
    return wrapper
