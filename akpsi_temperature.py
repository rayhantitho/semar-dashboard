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
flags.DEFINE_string('variable', 'thetao',
                    'Variable to download')
FLAGS = flags.FLAGS

import os, django,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.home.models import LocationLow, TemperatureLow

def main(date_min = None, date_max = None, variable = 'thetao'):
    if date_min is None or date_max is None:

        date_max = datetime.now() + timedelta(3)
        date_min = date_max - timedelta(2)

        date_max = date_max.strftime('%Y-%m-%d %H:00:00')
        date_min = date_min.strftime('%Y-%m-%d %H:00:00')
        
    output = subprocess.call(["./akpsi_temperature_job.sh",date_min , date_max, variable])
    return date_min, date_max

def execute(_):
    date_min, date_max = main(FLAGS.date_min, FLAGS.date_max, FLAGS.variable)
    netcdf_obj = xr.open_dataset("/home/rayhan/Extra/data/temperature2.nc")
    dct = {
        "time": [],
        "depth":[],
        "latitude":[],
        "longitude":[],
        "thetao":[]
    }
    df = netcdf_obj['thetao'].to_dataframe()
    df_fish = df.loc[(df.index.get_level_values('longitude') % 3 == 0) & (df.index.get_level_values('latitude') % 3 == 0)]
    df_temp = df.loc[(df.index.get_level_values('longitude') % 1 == 0) & (df.index.get_level_values('latitude') % 1 == 0)]
    df_fish = df_fish.dropna()
    df_temp = df_temp.dropna()
    for i in tqdm(range(df_fish.shape[0])):
        data = df_fish.iloc[i].name
        thetao = df_fish.iloc[i]['thetao']
        fishing = True if thetao > 30 else False
        if fishing:
            fish = LocationLow(latitude=data[2], longitude=data[3], fishing = fishing, date=data[0], thetao = thetao)
            fish.save()

    for i in tqdm(range(df_temp.shape[0])):
        data = df_temp.iloc[i].name
        thetao = df_temp.iloc[i]['thetao']
        temp = TemperatureLow(latitude=data[2], longitude=data[3], fishing = fishing, date=data[0], thetao = thetao)
        temp.save()
if __name__ == '__main__':
    app.run(execute)

