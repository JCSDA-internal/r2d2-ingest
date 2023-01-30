import sys
import subprocess

from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement
from solo.file_manager import FileManager


def convert_gfs(yaml_file):
    """
    Converts GFS background data files from one resolution (e.g., c768) to another resolution (e.g., c192) using the
    key/value pairs set in the supplied YAML file. This script dynamically creates a YAML file for the
    gfs_converter_orion.sh bash script which is set on the queue on Orion through a loop over dates.

    yaml_file - The path to this function's configuration file.
    """
    config = Configuration(yaml_file)
    dates = date_sequence(config.start_date, config.end_date, config.step_date)
    step_bkg = config.step_bkg
    start_res = config.start_res
    end_res = config.end_res
    start_np = config.start_np
    end_np = config.end_np

    input_path = f'{config.input_path}/{start_res}'
    output_path = f'{config.output_path}/{end_res}'
    yaml_path = f'{config.yaml_path}/{step_bkg}_{start_res}_{end_res}'

    file_manager = FileManager()
    file_manager.makedirs(output_path, exist_ok=True)
    file_manager.makedirs(yaml_path, exist_ok=True)

    for date in dates:
        date = JediDate(date)
        datetime = date + DateIncrement(step_bkg)
        input_prefix = f'gfs.oper.fc.{step_bkg}.{date}.{start_res}'
        output_prefix = f'gfs.oper.fc.{step_bkg}.{date}.{end_res}'
        input_date_path = f'{input_path}/{date}'
        output_date_path = f'{output_path}/{date}'
        file_manager.makedirs(output_date_path, exist_ok=True)
        template_file = open('gfs_converter_template.yaml', 'r')
        template_text = template_file.read()
        yaml_text = template_text.replace('{start_np}', start_np)
        yaml_text = yaml_text.replace('{end_np}', end_np)
        yaml_text = yaml_text.replace('{date}', str(date))
        yaml_text = yaml_text.replace('{datetime}', str(datetime))
        yaml_text = yaml_text.replace('{step_bkg}', step_bkg)
        yaml_text = yaml_text.replace('{input_date_path}', input_date_path)
        yaml_text = yaml_text.replace('{output_date_path}', output_date_path)
        yaml_text = yaml_text.replace('{input_prefix}', input_prefix)
        yaml_text = yaml_text.replace('{output_prefix}', output_prefix)
        yaml_file_path = f'{yaml_path}/gfs_converter_{date}_{step_bkg}_{start_res}_{end_res}.yaml'
        yaml_file = open(yaml_file_path, 'w')
        yaml_file.write(yaml_text)
        yaml_file.close()
        subprocess.run(['sbatch', 'gfs_converter_orion.sh', yaml_file_path])


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    convert_gfs(yaml_file)
