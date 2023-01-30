import sys

from r2d2 import fetch
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def fetch_bias_correction(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types

    for date in dates:
        date = JediDate(date)
        day = f'{date.year()}{date.month()}{date.day()}'
        hour = f'{date.hour()}'
        for obs_type in obs_types:
            fetch(
                type='bc',
                provider='noaa',
                model='gfs',
                experiment='oper',
                date=date,
                obs_type=obs_type,
                file_type='satbias',
                ignore_missing='no',
            )
            fetch(
                type='bc',
                provider='noaa',
                model='gfs',
                experiment='oper',
                date=date,
                obs_type=obs_type,
                file_type='tlapse',
                ignore_missing='no',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    fetch_bias_correction(yaml_file)
