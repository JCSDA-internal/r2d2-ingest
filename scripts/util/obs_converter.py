import os

from solo.basic_files import tree


def convert_observations():
    dir = "/Users/eric2/ncdiag/obs/PT6H/2021-08-02"
    for path, root, filename in tree(dir):
        if not filename.startswith("."):
            filepath = os.path.join(path, root, filename)
            convert_observation(path, root, filename)


def convert_observation(path, root, filename: str):
    filename_comps = filename.split('.')
    provider = filename_comps[0]
    window_length = filename_comps[3]
    obs_type = filename_comps[4]
    window_start = filename_comps[5]
    file_path = os.path.join(path, root, filename)
    new_filename = f'{provider}.obs.{window_length}.{obs_type}.{window_start}.nc4'
    new_filepath = os.path.join(path, root, new_filename)
    os.rename(file_path, new_filepath)


if __name__ == '__main__':
    convert_observations()
