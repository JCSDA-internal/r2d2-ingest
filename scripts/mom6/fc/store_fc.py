import sys

from r2d2 import store
from solo.configuration import Configuration
from solo.date import date_sequence, DateIncrement


def store_fc(yaml_file):
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    type = config.type
    model = config.model
    source_dir = config.source_dir
    step = config.step
    nc_file_types = config.nc_file_types
    nc_date_file_types = config.nc_date_file_types
    restart_file_name = config.restart_file_name
    step_secs = int(DateIncrement(step).total_seconds() / 2.0)

    for date in dates:
        day = str(date)[:8]
        day = day[:4] + '-' + day[4:6] + '-' + day[6:8]
        for nc_file_type in nc_file_types:
            if nc_file_type in nc_date_file_types:
                source_file_path = f'{source_dir}/{date}/ctrl/{nc_file_type}.{day}-{step_secs}.nc'
            else:
                source_file_path = f'{source_dir}/{date}/ctrl/{nc_file_type}.nc'
            store(
                model=model,
                type=type,
                step=step,
                database='local',
                date=date,
                file_type=nc_file_type,
                source_file=source_file_path,
            )
        store(
            model=model,
            type=type,
            step=step,
            database='local',
            date=date,
            file_type=restart_file_name,
            source_file=f'{source_dir}/{date}/ctrl/{restart_file_name}',
        )


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    store_fc(yaml_file)
