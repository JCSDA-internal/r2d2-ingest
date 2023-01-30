from r2d2 import fetch, date_sequence
from solo.logger import Logger
from solo.date import Day
from solo.configuration import Configuration

logger = Logger('ncdiag_fetch')
config = Configuration('config.yaml')
dates = date_sequence(config.start, config.end, config.step)
obs_types = config.obs_types

for date in dates:
    day = str(date).split('T')[0]
    day = Day(date)
    for obs_type in obs_types:
        fetch(
            provider='ncdiag',
            type='obs',
            database='archive',
            window_start=date,
            obs_type=obs_type,
            window_length='PT6H',
            target_file=f's3://eric-r2d2/$(provider)/$(type)/$(time_window)/{day}/$(provider).$(type).$(time_window).$(obs_type).$(date).nc4',
            ignore_missing='yes'
        )

