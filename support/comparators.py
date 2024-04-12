# -*- coding: utf-8 -*-

def compare_by_name_and_number(name1, number1, name2, number2):
    """
    Compares two names and two numbers. If they are the same, return True, else return False.
    :param name1: a string
    :param number1: an integer
    :param name2: a string
    :param number2: an integer
    :return: a boolean
    """
    # ToDo: 3. Added this:
    if name1 is None or name2 is None:
        if number1 != number2:
            return False
        return True

    # turn to lowercase
    name1 = name1.lower()
    name2 = name2.lower()

    if name1 != name2:
        return False
    if number1 != number2:
        return False
    return True
