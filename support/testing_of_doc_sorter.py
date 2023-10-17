import os
import shutil
import zipfile


source_folder = r'C:\Appl\Projects\Python\Folders to move\Work'
destination_folder = r'C:\Appl\Projects\Python\Folders to move\Finished'
archive_folder = r'C:\Appl\Projects\Python\Folders to move\Finished'

# os.makedirs(archive_folder, exist_ok=True)


def extract_revision(filename):
    parts = filename.split('_')
    revision = parts[1]
    return revision


def extract_file_name(filename):
    parts = filename.split('_')
    file_name = parts[0]
    return file_name


def archive_file(file_path):
    # Create an archive of the file
    file_name = os.path.basename(file_path)
    archive_name = os.path.splitext(file_name)[0] + ".zip"
    archive_path = os.path.join(archive_folder, archive_name)

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(file_path, os.path.basename(file_path))


def compare_and_replace_files(dir1, dir2):
    files_list1 = os.listdir(dir1)
    files_list2 = os.listdir(dir2)

    print(os.path.splitext(files_list1[0])[0])
    print(os.path.splitext(files_list2[0])[0])

    for file1 in files_list1:
        for file2 in files_list2:
            file1_filename = extract_file_name(file1)
            file2_filename = extract_file_name(file2)

            if file1_filename == file2_filename:
                file1_revision = extract_revision(file1)
                file2_revision = extract_revision(file2)

                if file1_revision > file2_revision:
                    file1_path = os.path.join(dir1, file1)
                    file2_path = os.path.join(dir2, file2)

                    print(f"Replacing {file2} with {file1}")

                    # Archive file2
                    archive_file(file2_path)
                    # Remove file2
                    os.remove(file2_path)
                    # Copy file1
                    shutil.copy(file1_path, os.path.join(dir2, file1))


compare_and_replace_files(source_folder, destination_folder)
