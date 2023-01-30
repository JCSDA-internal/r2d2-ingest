import os

from r2d2 import store
from solo.basic_files import tree


def store_forecast():
    source_dir = "/work/noaa/da/eric/r2d2_input_data/l95"
    input_file_paths = []
    for path, root, filename in tree(source_dir):
        if not filename.startswith("."):
            input_file_paths.append(os.path.join(path, root, filename))

    for file_path in input_file_paths:
        components = return_components(file_path)

        store(
            model=components['model'],
            type=components['type'],
            experiment=components['experiment'],
            resolution=components['resolution'],
            date=components['date'],
            step=components['step'],
            source_file=components['source_file'],
            file_format=components['file_format'],
            ignore_missing='no',
        )


def return_components(file_path: str):
    components = {'source_file': file_path}
    file_path_components = os.path.basename(file_path).split('.')
    components['resolution'] = '40'
    components['experiment'] = file_path_components[0]
    components['model'] = file_path_components[1]
    components['type'] = file_path_components[2]
    components['date'] = file_path_components[3]
    components['step'] = file_path_components[4]
    if file_path_components[5] == 'nc':
        components['file_format'] = 'netcdf'
    elif file_path_components[5] == 'l95':
        components['file_format'] = 'l95'
    return components


if __name__ == '__main__':
    store_forecast()

