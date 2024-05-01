# -*- coding: utf-8 -*-
import os
import zipfile
import shutil

from support.extractors import extract_text_after_last_backslash


def directory_exists(directory):
    """
    checks if a directory exists
    :param directory: the directory to check
    :return: True if the directory exists, False otherwise
    """
    return os.path.exists(directory)


def create_directory(directory):
    """
    creates a directory
    :param directory: the directory to create
    :return: None
    """
    try:
        os.makedirs(directory)
    except Exception as e:
        print(e)
        pass


def move_directory(source, destination):
    """
    moves a directory
    :param source: the source directory
    :param destination: the destination directory
    :return: None
    """
    shutil.move(source, destination)


def copy_directory(source, destination):
    """
    copies a directory
    :param source: the source directory
    :param destination: the destination directory
    :return: None
    """
    shutil.copytree(source, destination)


def delete_directory(directory):
    """
    deletes a directory
    :param directory: the directory to delete
    :return: None
    """
    # os.rmdir(directory)
    shutil.rmtree(directory)


def archive_directory(path_of_folder_to_archive, archive_folder):
    """
    Creates an archive of the folder
    :param path_of_folder_to_archive: the path of the folder to be archived
    :param archive_folder: the folder where the archive will be created
    """
    folder_name = extract_text_after_last_backslash(path_of_folder_to_archive)
    archive_name = folder_name + ".zip"
    archive_path = os.path.join(archive_folder, archive_name)

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for root, dirs, files in os.walk(path_of_folder_to_archive):
            for file in files:
                archive.write(os.path.join(root, file), os.path.join(folder_name, file))


def copy_file(source, destination):
    """
    copies a file
    :param source: the source file
    :param destination: the destination file
    :return: None
    """
    shutil.copy(source, destination)


def delete_file(file_path):
    """
    deletes a file
    :param file_path: the file to delete
    :return: None
    """
    os.remove(file_path)
