import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def store_bias_correction(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    source_path = config.source_path
    obs_types = config.obs_types

    for date in dates:
        date = JediDate(date)
        day = f'{date.year()}{date.month()}{date.day()}'
        hour = f'{date.hour()}'
        for obs_type in obs_types:
            store(
                type='bc',
                provider='noaa',
                experiment='oper',
                model='gfs',
                date=date,
                obs_type=obs_type,
                file_type='satbias',
                source_file=f'{source_path}/gdas.{day}/{hour}/atmos/{obs_type}_$(file_type).nc4',
                ignore_missing='no',
            )
            store(
                type='bc',
                provider='noaa',
                experiment='oper',
                model='gfs',
                date=date,
                obs_type=obs_type,
                file_type='tlapse',
                source_file=f'{source_path}/gdas.{day}/{hour}/atmos/{obs_type}_$(file_type).txt',
                ignore_missing='no',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_bias_correction(yaml_file)
