import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import JediDate, DateIncrement


def store_observations(yaml_file):
    config = Configuration(yaml_file)
    window_start = config.window_start
    source_file_date = config.source_file_date
    provider = config.provider
    type = config.type
    window_length = config.window_length
    source_path = config.source_path
    obs_type = config.obs_type
    window_start = JediDate(window_start) - DateIncrement('PT3H')

    store(
        provider=provider,
        type=type,
        window_start=window_start,
        obs_type=obs_type,
        window_length=window_length,
        source_file=f'{source_path}/{provider}/{type}/{obs_type}/{obs_type}_{provider}_{source_file_date}.nc4',
        ignore_missing='no',
    )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_observations(yaml_file)