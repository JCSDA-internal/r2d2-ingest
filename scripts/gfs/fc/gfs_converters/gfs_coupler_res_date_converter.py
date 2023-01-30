import sys

from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement


def convert_gfs_coupler_res_date(yaml_file):
    """
    Converts the second date listed in each PT6H coupler.res file copied from the PT3H coupler.res files by adding PT3H
    to this second date.

    yaml_file - The path to this function's configuration file.
    """
    config = Configuration(yaml_file)
    dates = date_sequence(config.start, config.end, config.step)
    resolution = config.resolution
    source_path = config.source_path

    for date in dates:
        date = JediDate(date)
        new_date = date + DateIncrement('PT6H')
        file_name = f'{date}.PT6H.coupler.res'
        file_path = f'{source_path}/{resolution}/{date}/{file_name}'
        file = open(file_path, 'r')
        file_text = file.read()
        file.close()
        file_lines = file_text.split('\n')
        file_lines[2] = get_new_line(new_date)
        delimiter = '\n'
        file_text = delimiter.join(file_lines)
        file = open(file_path, 'w')
        file.write(file_text)
        file.close()


def get_new_line(new_date):
    """
    Returns a new line of text using the provided new_date JediDate object.

    new_date - The new JediDate object used for the second date in the PT6H coupler.res files.
    """
    new_line = '{0:>6s}{1:>6d}{2:>6d}{3:>6d}     0     0        Current model time: year, month, day, hour, minute, ' \
               'second'.format(new_date.year(), int(new_date.month_int()), new_date.day_int(), new_date.hour_int())
    return new_line


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    convert_gfs_coupler_res_date(yaml_file)
