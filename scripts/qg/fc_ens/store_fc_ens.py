import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, DateIncrement, JediDate


def store_fc_ens(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.window_length)
    type = config.type
    model = config.model
    source_path = config.source_path
    step = config.step
    experiment = config.experiment
    resolution = config.resolution
    members = config.members

    for date in dates:
        date = JediDate(date)
        date_start = JediDate(date) + DateIncrement(step)

        for member in members:
            store(
                model=model,
                type=type,
                step=step,
                date=date_start,
                experiment=experiment,
                resolution=resolution,
                member=member,
                source_file=f'{source_path}/{model}/{type}/forecast.ens.{member}.{date}.{step}.nc',
            )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc_ens(yaml_file)
