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
flags.DEFINE_string('variable', 'chl',
                    'Variable to download')
FLAGS = flags.FLAGS

import os, django,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.home.models import ChlorophylLow

def main(date_min = None, date_max = None, variable = 'chl'):
    if date_min is None or date_max is None:

        date_max = datetime.now() + timedelta(3)
        date_min = date_max - timedelta(10)

        date_max = date_max.strftime('%Y-%m-%d %H:00:00')
        date_min = date_min.strftime('%Y-%m-%d %H:00:00')
        
    output = subprocess.call(["./akpsi_chlorophyl_job.sh",date_min , date_max, variable])
    return date_min, date_max

def execute(_):
    # date_min, date_max = main(FLAGS.date_min, FLAGS.date_max, FLAGS.variable)
    netcdf_obj = xr.open_dataset("/home/rayhan/Extra/data/chlorophyl.nc")
    df = netcdf_obj['chl'].to_dataframe()
    df = df.loc[(df.index.get_level_values('longitude') % 1 == 0) & (df.index.get_level_values('latitude') % 1 == 0)]
    df = df.fillna(0)

    for i in tqdm(range(df.shape[0])):
        data = df.iloc[i].name
        chl = df.iloc[i]['chl']
        temp = ChlorophylLow(latitude=data[2], longitude=data[3], fishing = True, date=data[0], chl = chl)
        temp.save()
if __name__ == '__main__':
    app.run(execute)

