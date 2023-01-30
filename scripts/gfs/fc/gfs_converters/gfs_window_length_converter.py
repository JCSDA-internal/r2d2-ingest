import shutil
import os
from solo.basic_files import tree


def convert_gfs_window_length():
    """
    Copies all PT3H GFS backgrounds to PT6H GFS backgrounds within the provided directory.
    """
    dir = "/work/noaa/da/jedipara/r2d2_archive_orion/gfs/fc/oper/c12"
    for path, root, filename in tree(dir):
        if not filename.startswith("."):
            convert(path, root, filename)


def convert(path, root, filename: str):
    """
    Copies the file provided at path, root, filename to its PT6H equivalent name.

    path, root, filename - The path components for the file to convert.
    """
    old_filepath = os.path.join(path, root, filename)
    new_filepath = os.path.join(path, root, filename.replace('PT3H', 'PT6H'))
    # Skip these dates since we already have PT6H files for them
    if '2021-08-01' not in old_filepath and '2021-07-31' not in old_filepath:
        shutil.copy(old_filepath, new_filepath)


if __name__ == '__main__':
    convert_gfs_window_length()
