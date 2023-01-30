import os
import sys

from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def convert_gfs_coupler_res_name(yaml_file):
    """
    Converts name provided by the fv3jedi_convertstate.x executable to the common filename used for the coupler.res
    for each date. For example, this executable creates a file based on the provided prefix in the YAML template file
    called gfs_converter_template.yaml. For example, this function converts
    'gfs.oper.fc.PT3H.<date>.<resolution>.coupler.res' to '<date>.PT3H.coupler.res'. This script must be executed
    for after the gfs_converter.py script.

    yaml_file - The path to this function's configuration file.
    """
    config = Configuration(yaml_file)
    dates = date_sequence(config.start_date, config.end_date, config.step_date)
    step_bkg = config.step_bkg
    resolution = config.resolution
    source_path = config.source_path

    for date in dates:
        date = JediDate(date)
        old_file_name = f'gfs.oper.fc.{step_bkg}.{date}.{resolution}.coupler.res'
        new_file_name = f'{date}.{step_bkg}.coupler.res'
        old_file_path = f'{source_path}/{resolution}/{date}/{old_file_name}'
        new_file_path = f'{source_path}/{resolution}/{date}/{new_file_name}'
        os.rename(old_file_path, new_file_path)


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    convert_gfs_coupler_res_name(yaml_file)