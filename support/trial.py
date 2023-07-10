# file_manager is currently only the code copied from dir_walker

# here i am trying some things from chatgpt first

import os
import shutil

# path where you want to create a new folder
path = r'C:\Users\User\Desktop\P1'

# name of the new folder
folder_name = 'NewFolder'

# full path of the new folder
full_path = os.path.join(path, folder_name)

# check if the folder already exists. If not, create it.
if not os.path.exists(full_path):
    os.makedirs(full_path)

# path of the file you want to move
file_to_move = r'C:\Users\User\Desktop\P1\file_to_move.xlsx'

# Check if the file name contains 'i'
if 'i' in os.path.basename(file_to_move):
    # new path for the file after moving
    new_path_move = os.path.join(full_path, os.path.basename(file_to_move))

    # move the file to the new folder
    shutil.move(file_to_move, new_path_move)

# path of the file you want to copy
file_to_copy = r'C:\Users\User\Desktop\P1\file_to_copy.docx'

# Check if the file name contains 'i'
if 'i' in os.path.basename(file_to_copy):
    # new path for the file after copying
    new_path_copy = os.path.join(full_path, os.path.basename(file_to_copy))

    # copy the file to the new folder
    shutil.copy(file_to_copy, new_path_copy)
