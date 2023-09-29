import time


def replace_lower_dashes_with_spaces(string):
    return string.replace("_", " ")


def time_measurement_decorator(some_function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = some_function(*args, **kwargs)
        end = time.time()
        measurement = end - start
        print(f"generated in: {measurement:.5f}")
        return result
    return wrapper
