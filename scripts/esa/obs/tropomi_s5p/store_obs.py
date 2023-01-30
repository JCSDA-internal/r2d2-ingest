import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement


def store_observations(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.window_length)
    provider = config.provider
    type = config.type
    window_length = config.window_length
    source_path = config.source_path
    obs_type = config.obs_type

    for date in dates:
        date = JediDate(date)
        window_start = date - DateIncrement('PT3H')
        for coltype in ['_total','_tropo']:
            store(
                provider=provider,
                type=type,
                window_start=window_start,
                obs_type=obs_type+coltype,
                window_length=window_length,
                source_file=f'{source_path}/TROPOMI_S5P_{date.year()}{date.month()}{date.day()}T{date.hour()}_NO2{coltype}.nc',
                ignore_missing='yes',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_observations(yaml_file)
