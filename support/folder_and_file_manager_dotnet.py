# -*- coding: utf-8 -*-
from support.constants import location_of_dll, dll_name
from support.dll_runner import DllRunner


"""
Path to the dll folder
"""
path = location_of_dll

"""
Name of the dll must be usable by python, not i.e. "09.Some text"
"""
name = dll_name

"""
[
    {
        'NamespaceName1': [
            'ClassName1',
            'ClassName2',
        ]
    },
    {
        'NamespaceName2': [
            'ClassName3',
            'ClassName4',
        ]
    },
]
"""

imports = [
    {
        'FolderAndFileManipulation': [
            'FolderFileLib',
        ]
    },
]

"""
Initialize the runner
"""
runner = DllRunner()
runner.register_dll(name, path)
runner.handle_imports(*imports)


"""
Use it
"""
new_instance = runner.FolderFileLib()


def create_directory_with_dotnet(dir_path):
    """
    creates a directory
    :param dir_path: the directory to create
    :return: None
    """
    new_instance.createDirectory(dir_path)


def delete_directory_with_dotnet(dir_path):
    """
    deletes a directory
    :param dir_path: the directory to delete
    :return: None
    """
    new_instance.deleteDirectory(dir_path)


def move_directory_with_dotnet(source_dir, destination_dir):
    """
    If the destination directory already exists, Directory.Move will move the source
    directory into the destination directory, effectively overwriting its contents.
    If you want to merge the contents of the source directory with the destination directory,
    you should handle the file and subdirectory copying manually before removing the source
    directory.
    :param source_dir: the source directory
    :param destination_dir: the destination directory
    :return: None
    """
    new_instance.moveDirectory(source_dir, destination_dir)


def copy_file_with_dotnet(source_dir, destination_dir):
    """
    copies a file, you need the current path + the file name and the destination path + the file name
    :param source_dir: the source directory
    :param destination_dir: the destination directory
    :return: None
    """
    new_instance.copyFile(source_dir, destination_dir)


def delete_file_with_dotnet(file_path):
    """
    deletes a file.
    :param file_path: the file to delete
    :return: None
    """
    new_instance.deleteFile(file_path)
