import os

from r2d2 import store
from solo.basic_files import tree


def store_feedback():
    source_dir = "/work/noaa/da/eric/r2d2_input_data/l95"
    input_file_paths = []
    for path, root, filename in tree(source_dir):
        if not filename.startswith("."):
            input_file_paths.append(os.path.join(path, root, filename))

    for file_path in input_file_paths:
        components = return_components(file_path)

        store(
            obs_type=components['obs_type'],
            type=components['type'],
            experiment=components['experiment'],
            window_start=components['window_start'],
            window_length=components['window_length'],
            file_format=components['file_format'],
            source_file=components['source_file'],
            ignore_missing='no',
        )


def return_components(file_path: str):
    components = {'source_file': file_path}
    file_path_components = os.path.basename(file_path).split('.')
    components['window_length'] = 'PT6H'
    components['experiment'] = file_path_components[0]
    components['model'] = file_path_components[1]
    components['type'] = file_path_components[2]
    if components['model'] == 'l95':
        components['obs_type'] = 'l95'
        components['date'] = file_path_components[3]
        components['file_format'] = file_path_components[4]
    else:
        components['obs_type'] = file_path_components[3]
        components['date'] = file_path_components[4]
        components['file_format'] = file_path_components[5]
    return components


if __name__ == '__main__':
    store_feedback()
