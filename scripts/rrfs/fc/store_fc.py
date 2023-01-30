import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence


def store_fc(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    type = config.type
    model = config.model
    source_dir = config.source_dir
    step = config.step
    experiment = config.experiment
    resolution = config.resolution
    file_types = config.file_types

    for date in dates:
        for file_type in file_types:
            store(
                model=model,
                type=type,
                step=step,
                database='local',
                date=date,
                experiment=experiment,
                resolution=resolution,
                fc_date_rendering='analysis',
                file_type=file_type,
                source_file=f'{source_dir}/{date}/{file_type}',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
