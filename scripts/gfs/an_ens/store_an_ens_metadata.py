import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def store_an_ens_metadata(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    type = config.type
    model = config.model
    source_dir = config.source_dir
    experiment = config.experiment
    resolution = config.resolution
    file_types = config.file_types
    members = config.members

    for date in dates:
        date = JediDate(date)
        for member in range(1, (members+1)):
            for file_type in file_types:
                store(
                    model=model,
                    type=type,
                    experiment=experiment,
                    date=date,
                    resolution=resolution,
                    file_type=file_type,
                    member=member,
                    source_file=f'file://{source_dir}/mem{str(member).zfill(3)}/{date.year()}{date.month()}{date.day()}.{date.hour()}0000.$(file_type)'
                )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_an_ens_metadata(yaml_file)
