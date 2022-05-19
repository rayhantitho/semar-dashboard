import subprocess
import argparse
import iso8601
import pandas as pd
from absl import app, flags
import xarray as xr
from tqdm import tqdm
from datetime import datetime, timedelta



flags.DEFINE_string('date_min', None,
                    'start date')
flags.DEFINE_string('date_max', None,
                    'end date')
flags.DEFINE_string('variable1', 'uo',
                    'Variable to download')
flags.DEFINE_string('variable2', 'vo',
                    'Variable to download')
FLAGS = flags.FLAGS

import os, django,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.home.models import CurrentLow

def main(date_min = None, date_max = None, variable1 = 'uo', variable2 = 'vo'):
    if date_min is None or date_max is None:

        date_max = datetime.now() + timedelta(3)
        date_min = date_max - timedelta(10)

        date_max = date_max.strftime('%Y-%m-%d %H:00:00')
        date_min = date_min.strftime('%Y-%m-%d %H:00:00')
        
    output = subprocess.call(["./akpsi_current_job.sh",date_min , date_max, variable1, variable2])
    return date_min, date_max

def execute(_):
    date_min, date_max = main(FLAGS.date_min, FLAGS.date_max, FLAGS.variable1, FLAGS.variable2)
    # netcdf_obj = xr.open_dataset("/home/rayhan/Extra/data/current.nc")
    # df = netcdf_obj[['uo','vo']].to_dataframe()
    # df = df.loc[(df.index.get_level_values('longitude') % 1 == 0) & (df.index.get_level_values('latitude') % 1 == 0)]
    # df = df.fillna(0)
    # for i in tqdm(range(df.shape[0])):
    #     data = df.iloc[i].name
    #     uo = df.iloc[i]['uo']
    #     vo = df.iloc[i]['vo']
    #     current = CurrentLow(latitude=data[2], longitude=data[3], fishing = False, date=data[0], uo = uo, vo = vo)
    #     current.save()

if __name__ == '__main__':
    app.run(execute)

