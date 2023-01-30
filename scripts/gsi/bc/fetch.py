from r2d2 import fetch, date_sequence
from solo.logger import Logger
from solo.date import Day
from solo.configuration import Configuration

logger = Logger('gsi_fetch')
config = Configuration('config.yaml')
dates = date_sequence(config.start, config.end, config.step)
obs_types = config.obs_types
file_types = config.file_types

for date in dates:
    day = str(date).split('T')[0]
    day = Day(date)
    for file_type in file_types:
        for obs_type in obs_types:
            fetch(
                provider='gsi',
                type='bc',
                experiment='oper',
                database='archive',
                date=date,
                file_type=file_type,
                obs_type=obs_type,
                target_file=f's3://eric-r2d2/$(provider)/$(type)/$(experiment)/{day}/$(provider).$(experiment).$(type).$(obs_type).$(date).$(file_type)',
                ignore_missing='yes'
            )