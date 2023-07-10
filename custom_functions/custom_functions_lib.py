import os


def replace_lower_dashes_with_spaces(string):
    return string.replace("_", " ")


def get_list_of_all_projects_in_the_dir(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".ap18"):
                result.append(os.path.join(root, file))
    return result
