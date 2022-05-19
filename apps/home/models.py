# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LocationLow(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    thetao = models.FloatField()
    date = models.DateTimeField()
    fishing = models.BooleanField()

class TemperatureLow(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    thetao = models.FloatField()
    date = models.DateTimeField()
    fishing = models.BooleanField()

class CurrentLow(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    uo = models.FloatField()
    vo = models.FloatField()
    date = models.DateTimeField()
    fishing = models.BooleanField()

class ChlorophylLow(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    chl = models.FloatField()
    date = models.DateTimeField()
    fishing = models.BooleanField()