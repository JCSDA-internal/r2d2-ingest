import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, DateIncrement, JediDate


def store_fc(yaml_file):
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
        date_start = JediDate(date) + DateIncrement('PT3H')
        window_start = f'{date_start.hour()}0000'

        for file_type in file_types:
            store(
                model=model,
                type=type,
                step=step,
                date=date,
                experiment=experiment,
                resolution=resolution,
                tile=[1, 2, 3, 4, 5, 6],
                file_type=file_type,
                fc_date_rendering='analysis',
                source_file=f'file://{source_dir}/gdas.{day}/{hour}/RESTART/{day}.{window_start}.$(file_type).tile$(tile).nc'
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
