import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, DateIncrement, JediDate


def store_fc_metadata(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.window_length)
    type = config.type
    model = config.model
    source_dir = config.source_dir
    step = config.step
    experiment = config.experiment
    resolution = config.resolution
    file_types = config.file_types

    for date in dates:
        date = JediDate(date)
        day = f'{date.year()}{date.month()}{date.day()}'
        hour = f'{date.hour()}'
        date_start = JediDate(date) + DateIncrement('PT6H')
        day_start = f'{date_start.year()}{date_start.month()}{date_start.day()}'
        window_start = f'{date_start.hour()}0000'

        for file_type in file_types:
            store(
                model=model,
                type=type,
                step=step,
                date=date,
                experiment=experiment,
                resolution=resolution,
                file_type=file_type,
                fc_date_rendering='analysis',
                source_file=f'{source_dir}/gdas.{day}/{hour}/RESTART/{day_start}.{window_start}.{file_type}.ges'
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc_metadata(yaml_file)
