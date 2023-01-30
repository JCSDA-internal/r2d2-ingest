import sys

from r2d2 import store, date_sequence
from solo.date import JediDate, DateIncrement
from solo.configuration import Configuration


def store_observations(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types
    provider = config.provider
    type = config.type
    time_window = config.time_window
    source_path = config.source_path

    for date in dates:
        file_date = date
        storage_date = JediDate(file_date) - DateIncrement('PT3H')
        for obs_type in obs_types:
            store(
                provider=provider,
                type=type,
                date=storage_date,
                obs_type=obs_type,
                time_window=time_window,
                source_file=f'{source_path}/{file_date}/IODA/obs/{obs_type}_obs_{file_date}.nc4',
                ignore_missing='yes',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_observations(yaml_file)
