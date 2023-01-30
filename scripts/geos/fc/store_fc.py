import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import DateIncrement, Date


def store_fc(yaml_file):
    config = Configuration(yaml_file)
    dates = config.dates
    source_dir = config.source_dir
    file_type = config.file_type
    source_steps = config.source_steps

    for date in dates:
        day = str(date).split('T')[0]
        for source_step in source_steps:
            step = DateIncrement(source_step)
            new_step_secs = step.total_seconds() - 10800
            new_step = DateIncrement(seconds=new_step_secs)
            new_date = Date(date) + DateIncrement('PT3H')
            store(
                model='geos',
                type='fc',
                experiment='x0044',
                step=new_step,
                database='local',
                date=new_date,
                resolution='c360',
                file_type=file_type,
                source_file=f'{source_dir}/$(model)/$(type)/$(experiment)/$(resolution)/{day}/$(model).$(experiment).$(type).{source_step}.{date}.{file_type}.nc'
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
