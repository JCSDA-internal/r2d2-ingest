import os

from r2d2 import store
from solo.basic_files import tree
from solo.date import JediDate, DateIncrement


def store_observation():
    source_dir = "/work/noaa/da/eric/r2d2_input_data/truth"
    input_file_paths = []
    for path, root, filename in tree(source_dir):
        if not filename.startswith("."):
            input_file_paths.append(os.path.join(path, root, filename))

    for file_path in input_file_paths:
        components = return_components(file_path)

        store(
            provider='truth',
            type=components['type'],
            obs_type=components['obs_type'],
            window_start=components['window_start'],
            window_length=components['window_length'],
            source_file=components['source_file'],
            file_format=components['file_format'],
            ignore_missing='no',
        )


def return_components(file_path: str):
    components = {'source_file': file_path}
    file_path_components = os.path.basename(file_path).split('.')
    components['window_length'] = 'PT6H'
    components['type'] = 'obs'
    components['model'] = file_path_components[1]
    components['window_start'] = JediDate(file_path_components[2]) - DateIncrement('PT3H')
    if components['model'] == 'l95':
        components['obs_type'] = 'l95'
        components['file_format'] = 'obt'
    else:
        components['obs_type'] = file_path_components[3]
        components['file_format'] = 'netcdf'
    return components


if __name__ == '__main__':
    store_observation()

