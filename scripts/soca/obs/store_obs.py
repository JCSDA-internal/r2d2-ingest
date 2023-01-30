import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence


def store_obs(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types
    provider = config.provider
    type = config.type
    source_dir = config.source_dir
    window_length = config.window_length

    for date in dates:
        day = str(date).split('T')[0]
        year = day[0:4]
        for obs_type in obs_types:
            obs_prefix = obs_type.split('_')[0]
            store(
                provider=provider,
                type=type,
                database='local',
                window_start=date,
                obs_type=obs_type,
                window_length=window_length,
                source_file=f'{source_dir}/{obs_prefix}/{year}/{day}/{obs_type}_{day}.nc',
                ignore_missing=True,
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_obs(yaml_file)
