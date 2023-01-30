import sys

from r2d2 import store
from solo.configuration import Configuration


def store_media(yaml_file):
    config = Configuration(yaml_file)
    window_start = config.window_start
    source_dir = config.source_dir
    type = config.type
    experiment = config.experiment
    window_length = config.window_length
    file_format = config.file_format
    plot_type = config.plot_type
    variables = config.variables
    obs_type = config.obs_type

    for variable in variables:
        store(
            window_start=window_start,
            type=type,
            experiment=experiment,
            window_length=window_length,
            file_format=file_format,
            plot_type=plot_type,
            variable=variable,
            obs_type=obs_type,
            source_file=f'{source_dir}/abi_g16_bt.{variable}.{window_start}.{file_format}',
            database='media',
            ignore_missing=False,
        )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_media(yaml_file)