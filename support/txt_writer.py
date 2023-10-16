def append_a_dict_to_txt_file(path_to_txt, contents_dictionary):
    with open(path_to_txt, 'a') as file:
        file.write('\n')
        for key, value in contents_dictionary.items():
            file.write(f'{key}: {value}\n')
    return f'Successfully exported to txt file in {path_to_txt}'


def append_a_string_to_txt_file(path_to_txt, string):
    with open(path_to_txt, 'a') as file:
        file.write('\n')
        file.write(string)
    return f'Successfully exported to txt file in {path_to_txt}'
