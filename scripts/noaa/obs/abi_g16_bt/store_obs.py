import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, DateIncrement, JediDate, Hour


def store_obs(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types
    provider = config.provider
    type = config.type
    source_dir = config.source_dir
    window_length = config.window_length

    for date in dates:
        date = Hour(date)
        window_start = str(JediDate(date) - DateIncrement('PT3H'))
        for obs_type in obs_types:
            store(
                provider=provider,
                type=type,
                database='local',
                window_start=window_start,
                obs_type=obs_type,
                window_length=window_length,
                source_file=f'{source_dir}/{date.month()}-{date.day()}-{date.year()}/{date.hour()}/{obs_type}.nc',
                ignore_missing=False,
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_obs(yaml_file)