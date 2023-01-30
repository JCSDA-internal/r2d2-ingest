from r2d2 import fetch

dates = ['2019-12-31T:18:00:00Z']

for date in dates:
    day = date.split('T')[0]
    fetch(
        model='l95',
        type='an',
        experiment='test',
        resolution='40',
        date=date,
        file_format='netcdf',
        target_file=f's3://eric-r2d2/$(model)/$(type)/$(experiment)/$(resolution)/{day}/l95.$(experiment).$(type).$(date).nc',
        database='archive',
        ignore_missing='yes'
    )
