import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement


def store_fc_ens_metadata(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.window_length)
    step = config.step
    type = config.type
    model = config.model
    source_dir = config.source_dir
    experiment = config.experiment
    resolution = config.resolution
    file_types = config.file_types
    first_member = int(config.first_member)
    last_member = int(config.last_member)
    for date in dates:
        window_begin = JediDate(date)
        window_mid= window_begin + DateIncrement(config.step)
        for member in range(first_member, last_member+1):
            for file_type in file_types:
                filename = f'file://{source_dir}/enkfgdas.{window_begin.year()}{window_begin.month()}{window_begin.day()}/{window_begin.hour()}/atmos/mem{str(member).zfill(3)}/RESTART/{window_mid.year()}{window_mid.month()}{window_mid.day()}.{window_mid.hour()}0000.$(file_type)'
                store(
                    model=model,
                    type=type,
                    experiment=experiment,
                    date=window_begin,
                    step=step,
                    resolution=resolution,
                    file_type=file_type,
                    fc_date_rendering='analysis',
                    member=member,
                    source_file=filename
                )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc_ens_metadata(yaml_file)
