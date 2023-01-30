import sys

from r2d2 import fetch, date_sequence
from solo.date import Day
from solo.configuration import Configuration


def fetch_observations(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types
    provider = config.provider
    type = config.type
    window_length = config.window_length
    target_path = config.target_path

    for date in dates:
        day = Day(date)
        for obs_type in obs_types:
            fetch(
                provider=provider,
                type=type,
                window_start=date,
                obs_type=obs_type,
                window_length=window_length,
                target_file=f'{target_path}/$(provider)/$(type)/$(experiment)/$(time_window)/{day}/$(provider).$('
                            f'experiment).$(type).$(time_window).$(obs_type).$(date).nc4',
                database='archive',
                ignore_missing='yes',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    fetch_observations(yaml_file)
