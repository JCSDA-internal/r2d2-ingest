from datetime import datetime

import pytz
import boto3
import argparse


def clean_s3_media(filter_date):
    bucket = 'r2d2.experiments.s3'
    s3 = boto3.client('s3', region_name='us-east-1')
    experiment_list = get_experiment_list(s3, bucket)
    for experiment in experiment_list:
        last_modified = get_last_modified(s3, bucket, experiment)
        if last_modified < pytz.UTC.localize(filter_date):
            print(f'Deleting experiment {experiment}.')
            delete_experiment(s3, bucket, experiment)
    print('This operation has completed.')


def get_last_modified(s3, bucket, experiment):
    objects = s3.list_objects(Bucket=bucket, Prefix=experiment)
    last_modified = objects['Contents'][0]['LastModified']
    return last_modified


def delete_experiment(s3, bucket, experiment):
    paginator = s3.get_paginator('list_objects')
    itr = paginator.paginate(Bucket=bucket, Prefix=experiment)
    for response in itr:
        files_to_delete = []
        files_in_folder = response["Contents"]
        for file in files_in_folder:
            files_to_delete.append({"Key": file["Key"]})
        s3.delete_objects(Bucket=bucket, Delete={"Objects": files_to_delete})


def get_experiment_list(s3, bucket):
    paginator = s3.get_paginator('list_objects')
    itr = paginator.paginate(Bucket=bucket, Delimiter='/')
    experiment_list = []
    for experiment in itr.search('CommonPrefixes'):
        experiment_list.append(experiment.get('Prefix')[:-1])
    return experiment_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filter_date', help='All experimental media data created before this date (exclusive) '
                                            'will be deleted. The date must be in the following format and '
                                            'encapsulated by double quotes: "2022-08-01 00:00:00"')
    args = parser.parse_args()
    filter_date = datetime.strptime(args.filter_date, '%Y-%m-%d %H:%M:%S')

    print(f'Attention! You are about to delete all experimental plots created before {filter_date}. '
          f'Do you want to proceed? [y/N]:')
    answer = input()
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        print('Please wait while this operation completes.')
        clean_s3_media(filter_date)
