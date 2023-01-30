import sys

from r2d2 import store
from solo.configuration import Configuration


def store_observations(yaml_file):
    config = Configuration(yaml_file)
    window_start = config.window_start
    provider = config.provider
    type = config.type
    window_length = config.window_length
    source_path = config.source_path
    obs_type = config.obs_type

    store(
        provider=provider,
        type=type,
        window_start=window_start,
        obs_type=obs_type,
        window_length=window_length,
        source_file=f'{source_path}/{provider}/{type}/{obs_type}/gnssro_PlanetiQ.nc4',
        ignore_missing='no',
    )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_observations(yaml_file)