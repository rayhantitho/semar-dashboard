# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from .models import LocationLow, TemperatureLow, CurrentLow, ChlorophylLow
from .forms import DateForm
import json
from datetime import datetime

import numpy as np
import math

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    json_data = LocationLow.objects.values('latitude', 'longitude', 'thetao')
    json_data = json.dumps(list(json_data))
    if request.method == "POST":
        form = DateForm(request.POST)
        json_data = LocationLow.objects.filter(date=form['date_time_field'].data).values('latitude', 'longitude', 'thetao')
        json_data = json.dumps(list(json_data))
        return render(request, 'home/index.html', {"data": json_data, "form":form})

    form = DateForm(request.POST)
    latest_date = LocationLow.objects.order_by('date').last().date
    json_data = LocationLow.objects.filter(date=latest_date).values('latitude', 'longitude', 'thetao')
    json_data = json.dumps(list(json_data))

    return render(request, 'home/index.html', {"data": json_data, "form":form}) 
    
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'ui-maps-chlorophyl.html':
            if request.method == "POST":
                form = DateForm(request.POST)
                json_data = ChlorophylLow.objects.filter(date = form['date_time_field'].data).values('latitude', 'longitude', 'chl')
                chlorophyl = []
                for point in json_data:
                    if point['chl'] > 0.3:
                        const = 500
                    else:
                        const = 60
                    point_data = [point['latitude'], point['longitude'], point['chl']*const]
                   
                    chlorophyl.append(point_data)

                chlorophyl = json.dumps(list(chlorophyl))
                return render(request, 'home/ui-maps-chlorophyl.html', {"data": chlorophyl, "form":form})
                
            form = DateForm(request.POST)
            print('Chlorophyl-----')
            latest_date = ChlorophylLow.objects.order_by('date').last().date
            print(latest_date)
            json_data = ChlorophylLow.objects.filter(date = latest_date).values('latitude', 'longitude', 'chl')
            chlorophyl = []
            for point in json_data:
                if point['chl'] > 0.3:
                    const = 500
                else:
                    const = 60
                point_data = [point['latitude'], point['longitude'], point['chl']*const]
                chlorophyl.append(point_data)
            
            chlorophyl = json.dumps(list(chlorophyl))
            return render(request, 'home/ui-maps-chlorophyl.html', {"data": chlorophyl , "form":form})

        if load_template == 'ui-maps-current.html':

            if request.method == "POST":
                form = DateForm(request.POST)
                json_data = CurrentLow.objects.filter(
                    date=form['date_time_field'].data
                    ).filter(
                    latitude__gte = -7, latitude__lte = -3
                    ).filter(longitude__gte = 107, longitude__lte = 118).values('latitude', 'longitude', 'uo', 'vo')

                dct_new = {}
                dct_new['parameterUnit'] = 'm.s-1'
                dct_new['parameterNumber'] = 2
                dct_new['parameterNumberName'] = 'Eastward current'
                dct_new['parameterCategory'] = 2
                dct_new['refTime'] = str(form['date_time_field'].data)
                dct_new['dx'] = 1
                dct_new['dy'] = 1
                dct_new['la1']  = -7
                dct_new['la2'] = -3
                dct_new['lo1'] = 107
                dct_new['lo2'] = 118
                dct_new['nx'] = math.ceil((dct_new['lo2'] - dct_new['lo1'] + 1)/dct_new['dx'])
                dct_new['ny'] = math.ceil((dct_new['la2'] - dct_new['la1'] + 1)/dct_new['dy'])

                dct_new2 = {}
                dct_new2['parameterUnit'] = 'm.s-1'
                dct_new2['parameterNumber'] = 3
                dct_new2['parameterNumberName'] = 'Northward current'
                dct_new2['parameterCategory'] = 2
                dct_new2['refTime'] = str(form['date_time_field'].data)
                dct_new2['dx'] = 1
                dct_new2['dy'] = 1
                dct_new2['la1']  = -7
                dct_new2['la2'] = -3
                dct_new2['lo1'] = 107
                dct_new2['lo2'] = 118
                dct_new2['nx'] = math.ceil((dct_new['lo2'] - dct_new['lo1'] + 1)/dct_new['dx'])
                dct_new2['ny'] = math.ceil((dct_new['la2'] - dct_new['la1'] + 1)/dct_new['dy'])

                uo = []
                vo = []
                for dt in json_data:
                    uo.append(dt['uo'])
                    vo.append(dt['vo'])
                uo = [x*50 for x in uo]
                vo = [x*50 for x in vo]
                dct_total = [{'header':dct_new, 'data':uo}, {'header':dct_new2, 'data':vo}]
                json_data = json.dumps(dct_total)
                with open('/home/rayhan/Works/kuliah/AKPSI/django-black-dashboard/apps/templates/home/current.json', 'w') as outfile:
                    json.dump(dct_total, outfile)
                return render(request, 'home/ui-maps-current.html', {"data": json_data, "form":form})

            form = DateForm(request.POST)
            print('Current----')
            latest_date = CurrentLow.objects.order_by('-date').first().date
            print(latest_date)
            json_data = CurrentLow.objects.filter(
                date=latest_date
                ).filter(
                latitude__gte = -7, latitude__lte = -3
                ).filter(longitude__gte = 107, longitude__lte = 118).values('latitude', 'longitude', 'uo', 'vo')

            dct_new = {}
            dct_new['parameterUnit'] = 'm.s-1'
            dct_new['parameterNumber'] = 2
            dct_new['parameterNumberName'] = 'Eastward current'
            dct_new['parameterCategory'] = 2
            dct_new['refTime'] = str(latest_date)
            dct_new['dx'] = 1
            dct_new['dy'] = 1
            dct_new['la1']  = -7
            dct_new['la2'] = -3
            dct_new['lo1'] = 107
            dct_new['lo2'] = 118
            dct_new['nx'] = math.ceil((dct_new['lo2'] - dct_new['lo1'] + 1)/dct_new['dx'])
            dct_new['ny'] = math.ceil((dct_new['la2'] - dct_new['la1'] + 1)/dct_new['dy'])

            dct_new2 = {}
            dct_new2['parameterUnit'] = 'm.s-1'
            dct_new2['parameterNumber'] = 3
            dct_new2['parameterNumberName'] = 'Northward current'
            dct_new2['parameterCategory'] = 2
            dct_new2['refTime'] = str(form['date_time_field'].data)
            dct_new2['dx'] = 1
            dct_new2['dy'] = 1
            dct_new2['la1']  = -7
            dct_new2['la2'] = -3
            dct_new2['lo1'] = 107
            dct_new2['lo2'] = 118
            dct_new2['nx'] = math.ceil((dct_new['lo2'] - dct_new['lo1'] + 1)/dct_new['dx'])
            dct_new2['ny'] = math.ceil((dct_new['la2'] - dct_new['la1'] + 1)/dct_new['dy'])

            uo = []
            vo = []
            for dt in json_data:
                uo.append(dt['uo'])
                vo.append(dt['vo'])
            uo = [x*50 for x in uo]
            vo = [x*50 for x in vo]
            dct_total = [{'header':dct_new, 'data':uo}, {'header':dct_new2, 'data':vo}]
 
            json_data = json.dumps(dct_total)
            with open('/home/rayhan/Works/kuliah/AKPSI/django-black-dashboard/apps/templates/home/current.json', 'w') as outfile:
                json.dump(dct_total, outfile)
            return render(request, 'home/ui-maps-current.html', {"data": json_data, "form":form})

        if load_template == 'ui-maps.html':
            if request.method == "POST":
                form = DateForm(request.POST)
                json_data = LocationLow.objects.filter(date=form['date_time_field'].data).values('latitude', 'longitude', 'thetao')
                json_data = json.dumps(list(json_data))
                return render(request, 'home/ui-maps.html', {"data": json_data, "form":form})

            form = DateForm(request.POST)
            print('Maps---')
            latest_date = LocationLow.objects.order_by('date').last().date
            print(latest_date)
            json_data = LocationLow.objects.filter(date=latest_date).values('latitude', 'longitude', 'thetao')
            json_data = json.dumps(list(json_data))

            return render(request, 'home/ui-maps.html', {"data": json_data, "form":form})
            
        if load_template == 'ui-maps-temperature.html':

            if request.method == "POST":
                form = DateForm(request.POST)
                json_data = TemperatureLow.objects.filter(date = form['date_time_field'].data).values('latitude', 'longitude', 'thetao')
                
                temperature = []
                lst = []
                for point in json_data:
                    lst.append(point['thetao'])
                scaled_temp = NormalizeData(lst)
                for point, tempr in zip(json_data, scaled_temp):
                    
                    if tempr < 0.65:
                        temper = tempr - 0.2
                    elif tempr < 0.73:
                        temper = tempr
                    elif tempr < 0.78:
                        temper = tempr + 4
                    elif tempr < 0.85:
                        temper = tempr + 12
                    else:
                        temper = tempr + 16

                    point_data = [point['latitude'], point['longitude'], temper*100]
                    temperature.append(point_data)
                temperature = json.dumps(list(temperature))
                return render(request, 'home/ui-maps-temperature.html', {"data": temperature, "form":form})
                
            form = DateForm(request.POST)
            print('Temperature---')
            latest_date = TemperatureLow.objects.order_by('date').first().date
            print(latest_date)
            json_data = TemperatureLow.objects.filter(date = latest_date).values('latitude', 'longitude', 'thetao')
            temperature = []
            lst = []
            for point in json_data:
                lst.append(point['thetao'])
            scaled_temp = NormalizeData(lst)
            for point, tempr in zip(json_data, scaled_temp):
                
                if tempr < 0.65:
                    temper = tempr + 0.1
                elif tempr < 0.73:
                    temper = tempr + 1
                elif tempr < 0.78:
                    temper = tempr + 6
                elif tempr < 0.85:
                    temper = tempr + 15
                else:
                    temper = tempr + 19
                point_data = [point['latitude'], point['longitude'], temper*100]
                temperature.append(point_data)
            temperature = json.dumps(list(temperature))
            return render(request, 'home/ui-maps-temperature.html', {"data": temperature, "form":form})

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist as e:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
