import sys

from r2d2 import fetch
from solo.configuration import Configuration


def fetch_fc(yaml_file):
    config = Configuration(yaml_file)
    dates = config.dates
    steps = config.steps
    file_type = config.file_type

    for date in dates:
        day = str(date).split('T')[0]
        for step in steps:
            fetch(
                model='geos',
                type='fc',
                experiment='x0044',
                step=step,
                database='shared',
                date=date,
                resolution='c360',
                file_type=file_type,
                target_file=f'/work/noaa/da/eric/jedi_app_background_data/$(model)/$(type)/$(experiment)/$(resolution)/{day}/$(model).$(experiment).$(type).$(step).$(date).{file_type}.nc',
                ignore_missing='yes'
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    fetch_fc(yaml_file)