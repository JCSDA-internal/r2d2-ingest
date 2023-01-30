import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, CoreDate, DateIncrement


def store_fc(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    type = config.type
    model = config.model
    source_dir = config.source_dir
    step = config.step
    experiment = config.experiment
    resolution = config.resolution

    for date in dates:
        path_date = CoreDate(date)
        file_date = CoreDate(date) + DateIncrement('PT6H')
        formatted_path_date = f'{path_date.year()}{path_date.month()}{path_date.day()}{path_date.hour()}'
        formatted_file_date = f'{file_date.year()}-{file_date.month()}-{file_date.day()}_{file_date.hour()}.00.00'
        store(
            model=model,
            type=type,
            step=step,
            database='local',
            window_start=date,
            experiment=experiment,
            resolution=resolution,
            fc_date_rendering='analysis',
            source_file=f'{source_dir}/{formatted_path_date}/mpasout.{formatted_file_date}.nc',
        )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
