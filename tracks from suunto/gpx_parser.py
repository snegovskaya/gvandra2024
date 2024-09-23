# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 23:48:09 2024

@author: ostap
"""

import gpxpy
import gpxpy.gpx
import pathlib
import matplotlib.pyplot as plt
import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
import numpy as np
import pandas as pd
from scipy import ndimage
from scipy import interpolate
from scipy import signal

import gpxpy
import gpxpy.gpx
from geopy.distance import great_circle
# Parsing an existing file:
# -------------------------


gpx_file = open('gvandra_merged_suunto.gpx', 'r')

gpx = gpxpy.parse(gpx_file)
gpx.reduce_points(10000)
# times = []
# elevations = []
# for track in gpx.tracks:
#     for segment in track.segments:
#         for point in segment.points:
#             times.append(point.time)
#             elevations.append(point.elevation)
#             # plt.plot(point.time, point.elevation)
#             # print(f'Point at ({point.time},{point.longitude}) -> {point.elevation}')
            
# plt.plot(elevations)


def get_data(gpx):
    '''Currently Only does the first track and first segment'''
    tzf = TimezoneFinder()
    # Use lists for the data not a DataFrame
    lat = []
    lon = []
    ele = []
    time = []
    n_trk = len(gpx.tracks)
    for trk in range(n_trk):
        n_seg = len(gpx.tracks[trk].segments)
        first = True  # Flag to get the timezone for this track
        for seg in range(n_seg):
            points = gpx.tracks[trk].segments[seg].points
            for point in points:
                if(first):
                    # Get the time zone from the first point in first segment
                    tz_name = tzf.timezone_at(lng=point.longitude, lat=point.latitude)
                    first = False
                lat.append(point.latitude)
                lon.append(point.longitude)
                ele.append(point.elevation)
                try:
                    new_time = point.time.astimezone(ZoneInfo(tz_name))
                except:
                    new_time = point.time.astimezone(ZoneInfo('UTC'))
                time.append(new_time)
    return lat, lon, ele, time

# %%
_, _, elevations, times = get_data(gpx)
plt.plot(times, elevations)

# %%
df = pd.DataFrame([] , index = [], columns = ['time','seconde', 'lat', 'long',
                                              'elevation','dist'])
i=0
t0 = gpx.tracks[0].segments[0].points[0].time
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if i==0:
                df.loc[i]=[(point.time-t0),(point.time-t0).seconds,
                           point.latitude, point.longitude, point.elevation,0.]
            else:
                dist = df.dist[i-1] + great_circle((point.latitude,
                                                    point.longitude),
                                                   (df.lat[i-1],df.long[i-1])).km
                df.loc[i]=[(point.time-t0),(point.time-t0).seconds,
                           point.latitude, point.longitude, point.elevation,dist]
            i=i+1
            
# %%
passes = {
    'Уллу-Кёль Вост.': {
        'point_num': 200,
        'elevation': 3_180,
        },
    
    'Джалпаккол Сев.': {
        'point_num': 1_800,
        'elevation': 3_550,
        },
    
    'Кичкинекол Мал.': {
        'point_num': 2_400,
        'elevation': 3_390,
        },
    
    'Перемётный': {
        'point_num': 3_100,
        'elevation': 3_250,
        },
    
    'Хотютау': {
        'point_num': 5_800,
        'elevation': 3_500,
        },
    
    'т/б \"Глобус\"': {
        'point_num': 900,
        'elevation': 1_550,
        },
    
    'а/л \"Узункол\"': {
        'point_num': 2_100,
        'elevation': 1_800,
        },
    
    'Актюбе': {
        'point_num': 4_550,
        'elevation': 1_450,
        },
}





# %% distance plot

fig, ax = plt.subplots(figsize=(15, 6))
my_params = {'font.size':24}
plt.rcParams.update(my_params)
ax.plot(df.dist,df.elevation,'b',label = "Elevation",
        linewidth=5)
ax.set_xlabel("Расстояние, км")
ax.set_ylabel("Высота, м")
# ax.grid()
ax.set_ylim(1400, 3700)
ax.set_xlim(0, 120)
for count, name in enumerate(passes.keys()):
    ax.annotate(name, (df.dist.iloc[passes[name]['point_num']],
                       passes[name]['elevation']))
    
# %% time plot

fig, ax = plt.subplots(figsize=(15, 6))
my_params = {'font.size':24}
plt.rcParams.update(my_params)
ax.plot(times ,elevations,'b',label = "Elevation",
        linewidth=5)
ax.set_xlabel("Время, дни")
ax.set_ylabel("Высота, м") 
raw_days_list = [datetime.day for datetime in times] 
days_list = 
ax.set_xticks([datetime.day for datetime in times].)
# ax.grid()
ax.set_ylim(1400, 3700)
# ax.set_xlim(0, 120)
for count, name in enumerate(passes.keys()):
    ax.annotate(name, (times[passes[name]['point_num']],
                       passes[name]['elevation']))

# %%
# fig.savefig('../pics/elevation_vs_time.pdf')