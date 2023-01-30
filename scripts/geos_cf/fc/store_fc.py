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
    file_type = config.file_type
    source_steps = config.source_steps
    window_length = config.window_length
    experiment = config.experiment
    resolution = config.resolution

    for date in dates:
        date = JediDate(date)
        for source_step in source_steps:
            ndate = JediDate(date) + DateIncrement(source_step)
            day = f'{ndate.year()}{ndate.month()}{ndate.day()}'
            hour = f'{ndate.hour()}'
            store(
                model=model,
                type=type,
                experiment=experiment,
                step=source_step,
                date=date,
                resolution=resolution,
                file_type=file_type,
                source_file=f'{source_dir}/geoscf_$(resolution).gcc_jedi.{day}_{hour}00z.nc4'
            )

if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
