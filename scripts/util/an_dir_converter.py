import os
import sys

from solo.basic_files import tree
from solo.file_manager import FileManager


def convert_an_dir(dir):
    for path, root, filename in tree(dir):
        if not filename.startswith("."):
            filepath = os.path.join(path, root, filename)
            if 'coupler.res' not in filename:
                convert(filepath, filename)


def convert(filepath: str, filename: str):
    filename_comps = filename.split('.')
    filepath_comps = filepath.split('/')
    filepath_comps[-2] = filename_comps[3]
    new_filepath = '/' + os.path.join(*filepath_comps)
    file_manager = FileManager()
    print(filepath)
    print(new_filepath)
    file_manager.copy(filepath, new_filepath)


if __name__ == '__main__':
    convert_an_dir(sys.argv[1])

