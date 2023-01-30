import sys
import subprocess

from solo.configuration import Configuration
from solo.date import date_sequence, JediDate


def convert_gfs_bc(yaml_file):
    config = Configuration(yaml_file)
    input_dir = config.input_dir
    dates = date_sequence(config.start, config.end, config.step)
    obs_types = config.obs_types

    satbias_converter_tmpl = config['satbias converter']['template']
    satbias_converter_exec = config['satbias converter']['executable']

    for date in dates:
        date = JediDate(date)
        day = f'{date.year()}{date.month()}{date.day()}'
        hour = f'{date.hour()}'
        for obs_type in obs_types:

            template_file = open(satbias_converter_tmpl, 'r')
            yaml_text = template_file.read()
            yaml_text = yaml_text.replace('{input_coeff_file}', f'{input_dir}/gdas.{day}/{hour}/atmos/gdas.t{hour}z.abias')
            yaml_text = yaml_text.replace('{input_err_file}', f'{input_dir}/gdas.{day}/{hour}/atmos/gdas.t{hour}z.abias_pc')
            yaml_text = yaml_text.replace('{output_file}', f'{input_dir}/gdas.{day}/{hour}/atmos/{obs_type}_satbias.nc4')
            yaml_text = yaml_text.replace('{sensor}', obs_type)
            yaml_file_path = f'{input_dir}/gdas.{day}/{hour}/atmos/satbias2ioda_{date}_{obs_type}.yaml'
            yaml_file = open(yaml_file_path, 'w')
            yaml_file.write(yaml_text)
            yaml_file.close()
            subprocess.run([satbias_converter_exec, yaml_file_path])

            with open(f'{input_dir}/gdas.{day}/{hour}/atmos/{obs_type}_tlapse.txt', 'w') as fileout:
                with open(f'{input_dir}/gdas.{day}/{hour}/atmos/gdas.t{hour}z.abias') as filein:
                    for line in filein:
                        if obs_type in line:
                            line_split = line.split()
                            fileout.write(f"{' '.join(line_split[1:4])}\n")


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    convert_gfs_bc(yaml_file)
