import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def store_observations(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.window_length)
    provider = config.provider
    type = config.type
    window_length = config.window_length
    source_path = config.source_path
    obs_type = config.obs_type

    for date in dates:
        window_start = JediDate(date)
        store(
            provider=provider,
            type=type,
            window_start=window_start,
            obs_type=obs_type,
            window_length=window_length,
            source_file=f'{source_path}/{provider}/{type}/{obs_type}/{window_start.year()}{window_start.month()}{window_start.day()}T{window_start.hour()}Z_{window_length}_{obs_type}.nc4',
            ignore_missing='no',
        )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_observations(yaml_file)
