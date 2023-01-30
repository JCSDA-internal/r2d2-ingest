import sys

from solo.file_manager import FileManager
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement


def download_gfs(yaml_file):
    config = Configuration(yaml_file)
    download_dir = config.download_dir
    dates = date_sequence(config.start, config.end, config.step)
    gfs_file_types = config.gfs_file_types
    file_manager = FileManager

    for date in dates:
        date = JediDate(date)
        day = f'{date.year()}{date.month()}{date.day()}'
        hour = f'{date.hour()}'
        date_start = JediDate(date) + DateIncrement('PT3H')
        window_start = f'{date_start.hour()}0000'
        for gfs_file_type in gfs_file_types:
            file_name = f'{day}.{window_start}.{gfs_file_type}'
            source = f's3://noaa-gfs-warmstart-pds/gdas.{day}/{hour}/RESTART/{file_name}'
            target = f'file://{download_dir}/gdas.{day}/{hour}/RESTART/{file_name}'
            file_manager.copy(source, target)


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    download_gfs(yaml_file)
