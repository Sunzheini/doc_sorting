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


def first_date_is_newer(date1, date2):
    """
    Compares two dates, i.e. 17102023 should be older than 09022024
    :param date1: a string
    :param date2: a string
    :return: a boolean
    """
    # There is a case when the date is not 17102023 but 17.10.2023 and after the regex, this function only receives 17
    if len(date1) != 8 or len(date2) != 8:
        raise ValueError("The date must be in the format ddmmyyyy")

    day1, month1, year1 = int(date1[0:2]), int(date1[2:4]), int(date1[4:])
    day2, month2, year2 = int(date2[0:2]), int(date2[2:4]), int(date2[4:])

    if year1 > year2:
        return True
    if year1 < year2:
        return False
    if month1 > month2:
        return True
    if month1 < month2:
        return False
    if day1 > day2:
        return True
    return False
