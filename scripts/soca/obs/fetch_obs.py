import sys

from r2d2 import fetch
from solo.configuration import Configuration
from solo.date import date_sequence


def fetch_obs(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types
    provider = config.provider
    type = config.type
    target_dir = config.target_dir
    window_length = config.window_length

    for date in dates:
        for obs_type in obs_types:
            target_file_name = "my_target_filename"
            fetch(
                provider=provider,
                type=type,
                database='shared',
                window_start=date,
                obs_type=obs_type,
                window_length=window_length,
                target_file=f'{target_dir}/{target_file_name}.nc4',
                ignore_missing=True,
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    fetch_obs(yaml_file)