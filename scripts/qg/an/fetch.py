from r2d2 import fetch

dates = ['2020-06-23T:18:00:00Z']

for date in dates:
    day = date.split('T')[0]
    fetch(
        model='qg',
        type='an',
        experiment='ref',
        resolution='40x20',
        date=date,
        file_format='netcdf',
        target_file=f's3://eric-r2d2/$(model)/$(type)/$(experiment)/$(resolution)/{day}/$(model).$(experiment).$(type).$(date).nc',
        database='archive',
        ignore_missing='yes'
    )
