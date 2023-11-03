# -*- coding: utf-8 -*-
"""
Created on Mon Jun 03 14:26:05 2013

@author: ryan
"""

import numpy as np
import pandas as pd
import csv
import os
from collections import defaultdict
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import random
import datetime
import pdb
from sklearn import ensemble
import time
import ephem
import pdb
from fuzzywuzzy import process
import seaborn as sns; sns.set()
from energyPATHWAYS import util
from pandas.tseries.holiday import get_calendar
from sklearn.linear_model import LinearRegression
import pytz
import datetime as DT

directory = r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Annual Refresh\pre 2020\Pathways\shape data\v2'
weather_locations = pd.read_csv(os.path.join(directory, 'process_solar_profiles', 'TMY3_StationsMeta.csv'), index_col=0)

cooling_degree_days_TMY3 = pd.read_csv(os.path.join(directory, 'weather data', 'cooling_degree_days_TMY3.csv'))
heating_degree_days_TMY3 = pd.read_csv(os.path.join(directory, 'weather data', 'heating_degree_days_TMY3.csv'))

# heat_pump_cop_curve = pd.read_csv(os.path.join(directory, 'weather data', '2020-07_heat_pump_cop_curve_low-tech.csv'), index_col=0)
heat_pump_cop_curve = pd.read_csv(os.path.join(directory, 'weather data', '2020-07_heat_pump_cop_curve.csv'), index_col=0)


def read_degree_day_data(path, tmy=False):
    data = []
    with open(path, 'r') as infile:
        csvreader = csv.reader(infile, delimiter='|')
        for i in range(3):
            next(csvreader)
        dates = next(csvreader)
        if tmy:
            data.append(['Region ID'] + [row for row in dates[1:]])
        else:
            data.append(['Region ID'] + [datetime.date(int(row[:4]), int(row[4:6]), int(row[6:])) for row in dates[1:]])
        for row in csvreader:
            data.append([int(r) for r in row])

    data = pd.DataFrame(data[1:], columns=data[0])
    data['type'] = type
    data = data.set_index(['Region ID', 'type'])
    data.columns.name = 'Date'
    data = data.stack().to_frame()
    data.columns = ['degree-days']
    return data

degree_days = pd.DataFrame()
for year in range(2010, 2013):
    for type in ['Cooling', 'Heating']:
        path = os.path.join(directory, 'weather data', 'noaa HDD CDD', 'DD', '{}.ClimateDivisions.{}.txt'.format(year, type))
        data = read_degree_day_data(path)
        degree_days = pd.concat((degree_days, data))

'''
COMMERCIAL HVAC
'''

def get_solar_angles(geography):
    site_info = weather_locations.loc[geographies[geography]]
    return _get_solar_angles(str(site_info['Latitude']), str(site_info['Longitude']), '2006/01/01 00:30:00', site_info['TZ'], 8760)

def _get_solar_angles(lat, lon, start_date, TZ, num_hr):
    sun = ephem.Sun()
    obs = ephem.Observer()
    obs.lat, obs.lon = lat, lon #needs to be strings
    obs.date = start_date
    obs.date -= ephem.hour * TZ
    # obs.elev = site_info['Elev']
    alt, az = [], []
    for i in range(num_hr):
        sun.compute(obs)
        alt.append(sun.alt)
        az.append(sun.az - np.pi)
        obs.date += ephem.hour
    return alt, az

def get_degree_days(geography):
    USAF = geographies[geography]
    DD = heating_degree_days_TMY3[str(USAF)].to_frame()
    DD.columns = ['HDD']
    DD['HDD 1'] = DD['HDD'].shift(-1)
    DD['HDD -1'] = DD['HDD'].shift(1)
    DD['HDD -2'] = DD['HDD'].shift(2)
    DD['HDD mean'] = DD['HDD'].mean()

    DD['CDD'] = cooling_degree_days_TMY3[str(USAF)]
    DD['CDD 1'] = DD['CDD'].shift(-1)
    DD['CDD -1'] = DD['CDD'].shift(1)
    DD['CDD -2'] = DD['CDD'].shift(2)
    DD['CDD mean'] = DD['CDD'].mean()
    DD = DD.ffill().bfill()
    DD['date'] = pd.date_range('1/1/2006', periods=365, freq='D')
    DD['USAF'] = USAF
    DD = DD.set_index(['USAF', 'date'])
    DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'HDD mean', 'CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'CDD mean']]
    return DD

def heat_pump_special_calc(df, geography):
    heating_load = df
    temperature = get_hourly_temperatures(geography)
    temperature_round = temperature.round()

    hourly_cop = np.array([heat_pump_cop_curve.loc[temp,'COP'].values[0] for temp in temperature_round.values])
    kwh = 1/hourly_cop * heating_load
    kwh = pd.DataFrame(kwh).clip(0, None, axis=1)

    # #### special for hybrid systems
    # UTILITY_FACTOR = 0.5
    # sorted_heating_load = np.sort(kwh.values.flatten())
    # cum_sum_heating = np.cumsum(sorted_heating_load)
    # total_heating_load = cum_sum_heating[-1]
    # heating_cut = np.nonzero(cum_sum_heating > total_heating_load * UTILITY_FACTOR)[0][0]
    # max_electric_heating = sorted_heating_load[heating_cut]
    # kwh[kwh > max_electric_heating] = 0 # when we want to get electricity
    # # kwh[kwh < max_electric_heating] = 0 # when we want to get pipeline gas
    # ####

    print (geography, kwh.max().max(), np.percentile(temperature.values.flatten()[np.nonzero(kwh.values.flatten())], .01))
    return kwh.values.flatten()

def get_hourly_temperatures(geography):
    file_name = 'Electric_Furnace_0.99_AFUE_RoomAC_EER_11.5.csv'
    profile_path = os.path.join(directory, 'weather data', 'NREL_load_shapes', 'ElecHomeResults', 'ElecHomeResults', 'Hourly', res_geo_map[geography], file_name)
    temp = pd.read_csv(profile_path, index_col=False)
    temp.columns = [c.split(' - ')[1] if ' - ' in c else c for c in temp.columns]
    df = temp.iloc[1:].astype(float)
    df = df[['Weather|Outdoor Drybulb']]
    return df

def get_load_data(profile_type, geography):
    prof_col = profile_types[profile_type]['profile_name']+'|CZ-'+geography
    data = pd.DataFrame(index=pd.date_range(start=datetime.datetime(2006, 1, 1), periods=8760, freq='60min'))
    data.index.names = ['datetime']
    if profile_type=='furnace_com':
        data[geographies[geography]] = heat_pump_special_calc(average_load_profiles[prof_col].values, geography)
    else:
        data[geographies[geography]] = average_load_profiles[prof_col].values
    data['hour'] = data.index.hour
    data['date'] = data.index.date
    data['USAF'] = geographies[geography]
    data = data.set_index(['USAF', 'date', 'hour'], append=True)
    data.index = data.index.droplevel('datetime')
    data = data.squeeze().unstack('hour')
    return data

def get_moisture_type(geography):
    # A is moist, B is dry, C is marine
    code = geography.split('_')[0][-1]
    return _get_moisture_type(code)

def _get_moisture_type(code):
    if code=='A':
        return 1
    elif code=='C':
        return 2
    else:
        return 3

def lock_id(id, lock_type):
    base_path = os.path.join(directory, 'locks')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    path = os.path.join(base_path, '{}.{}'.format(id, lock_type))
    with open(path, 'wb') as lock_file:
        csvwriter = csv.writer(lock_file, delimiter=',')
        csvwriter.writerow([str(datetime.datetime.today()).split('.')[0].replace(':', '.')])

def has_lock(id):
    if os.path.isfile(os.path.join(directory, 'locks', '{}.{}'.format(id, 'start'))) or \
        os.path.isfile(os.path.join(directory, 'locks', '{}.{}'.format(id, 'finish'))):
        return True
    else:
        return False

profile_types = {
'chiller_com':    {'file_name':'average_load_profiles', 'profile_name':'Chiller', 'shape_id':'50'},
'dx_ac_com':      {'file_name':'average_load_profiles', 'profile_name':'DX AC', 'shape_id':'51'},
'boiler_com':     {'file_name':'average_load_profiles', 'profile_name':'Boiler', 'shape_id':'52'},
'furnace_com':    {'file_name':'average_load_profiles', 'profile_name':'Furnace', 'shape_id':'53'}
}

geographies = {
'1A': 722020,
'2A': 722430,
'2B': 722780,
'3A': 723340,
'3B': 722700,
'3C': 724940,
'4A': 724060,
'4B': 723650,
'4C': 726940,
'5A': 725300,
'5B': 726810,
'6A': 726170,
'6B': 727720,
'7A': 727450,
'8A': 702610
}

res_geo_map = {
'1A': '1A_Miami',
'2A': '2A_Houston',
'2B': '2B_Phoenix',
'3A': '3A_Atlanta',
'3B': '3B-Coast_Los Angeles',
'3C': '3C_San Francisco',
'4A': '4A_Baltimore',
'4B': '4B_Albuquerque',
'4C': '4C_Seattle',
'5A': '5A_Chicago',
'5B': '5B_Boulder',
'6A': '6A_Minneapolis',
'6B': '6B_Helena',
'7A': '7_Duluth',
'8A': '8_Fairbanks'
}


base_path = os.path.join(directory, 'weather data', 'NREL_load_shapes', 'average_load_profiles')
average_load_profiles = pd.read_csv(os.path.join(base_path, 'average_load_profiles.csv'), index_col=False)*10000

validating_size = .01

fits = {}
predictor = {}
for profile_type in profile_types:
    if profile_type != 'furnace_com':
        continue
    h_or_c = 'Cooling' if profile_type in ('chiller_com', 'dx_ac_com') else 'Heating'

    fits[profile_type] = {}
    x = pd.DataFrame()
    y = pd.DataFrame()

    for geography in geographies:
        print( profile_type, geography, get_moisture_type(geography))
        load_data = get_load_data(profile_type, geography)
        DD = get_degree_days(geography)
        DD['dayofweek'] = DD.index.get_level_values('date').dayofweek
        DD['month'] = DD.index.get_level_values('date').month

        # if h_or_c == 'Cooling':
        #     DD = DD[['CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'moisture_type', 'dayofweek', 'month']]
        # elif h_or_c == 'Heating':
        #     DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'moisture_type', 'dayofweek', 'month']]

        alt, az = get_solar_angles(geography)
        # columns = ['alt_{}'.format(h) for h in range(1,25)] + ['az_{}'.format(h) for h in range(1,25)]
        # solar = pd.DataFrame(np.hstack((np.reshape(alt, (365, 24)), np.reshape(az, (365, 24)))), index=DD.index, columns=columns)
        # solar['max_alt'] = np.max(np.reshape(alt, (365, 24)), axis=1)
        solar = pd.DataFrame(np.max(np.reshape(alt, (365, 24)), axis=1), columns=['max_alt'], index=DD.index)
        # for h in range(1,24):
        #     solar[str(h)] = h

        x = pd.concat((x, pd.concat((DD, solar), axis=1)))
        y = pd.concat((y, load_data))

    shuffle = np.arange(len(x))
    np.random.shuffle(shuffle)
    training_size = int((1-validating_size)*len(x))
    i_train = shuffle[:training_size]
    i_validate = shuffle[training_size:]

    regr = ensemble.RandomForestRegressor(n_estimators=1000, verbose=1, n_jobs=-1)
    regr = regr.fit(x.values[i_train], y.values[i_train])
    fits[profile_type]['train'] = regr.score(x.values[i_train], y.values[i_train])
    fits[profile_type]['validate'] = regr.score(x.values[i_validate], y.values[i_validate])
    print('{} train = {}, validate = {}'.format(profile_type, fits[profile_type]['train'], fits[profile_type]['validate']))
    y_predicted_validate = regr.predict(x.values[i_validate])
    y_predicted_train = regr.predict(x.values[i_train])
    y_predicted = regr.predict(x.values)
    predictor[profile_type] = regr



start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2019, 12, 31)
cal = get_calendar('USFederalHolidayCalendar')  # possible to change to other holiday systems in config
holidays = [stamp.date() for stamp in cal.holidays(start=start_date, end=end_date)]


def get_degree_days_nuts(location):
    cdd = pd.read_csv(os.path.join(dd_dir, 'cdd', location + '.csv'), index_col=0, parse_dates=True)
    hdd = pd.read_csv(os.path.join(dd_dir, 'hdd', location+'.csv'), index_col=0, parse_dates=True)
    DD = pd.concat([cdd, hdd], axis=1)
    DD.columns = ['CDD', 'HDD']
    DD['HDD 1'] = DD['HDD'].shift(-1)
    DD['HDD -1'] = DD['HDD'].shift(1)
    DD['HDD -2'] = DD['HDD'].shift(2)
    DD['HDD mean'] = DD['HDD'].mean()

    DD['CDD 1'] = DD['CDD'].shift(-1)
    DD['CDD -1'] = DD['CDD'].shift(1)
    DD['CDD -2'] = DD['CDD'].shift(2)
    DD['CDD mean'] = DD['CDD'].mean()
    DD = DD.ffill().bfill()
    DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'HDD mean', 'CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'CDD mean']]
    DD = DD[DD.index.isin(pd.date_range(start_date, end_date, freq='D'))]
    return DD


coord = pd.read_csv(r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\Geographies\shapefile\nuts1_coord.csv')
coord = coord[['NUTS_ID', 'long', 'lat']]

spatial_join = pd.read_csv(r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\profiles\GeographiesSpatialJoin.csv')

dd_dir = r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\profiles\hdd_cdd_regression'

for profile_type in profile_types:
    if profile_type != 'furnace_com':
        continue
    h_or_c = 'Cooling' if profile_type in ('chiller_com', 'dx_ac_com') else 'Heating'
    data = []
    for i, location in coord.iterrows():
        if location['NUTS_ID'].lower() not in spatial_join['nuts1'].values:
            continue
        DD = get_degree_days_nuts(location['NUTS_ID'])
        DD['dayofweek'] = pd.DatetimeIndex(DD.index).dayofweek
        DD['month'] = pd.DatetimeIndex(DD.index).month

        tz = pytz.timezone(spatial_join[spatial_join['nuts1']==location['NUTS_ID'].lower()]['time zone'].unique()[0])
        offset = (tz.utcoffset(DT.datetime(2015, 1, 1)) + tz.dst(DT.datetime(2015, 1, 1))).total_seconds() / 3600.

        alt, az = _get_solar_angles(lat=str(location['lat']), lon=str(location['long']), start_date='2015/01/01 00:30:00', TZ=offset, num_hr=43824)
        solar = pd.DataFrame(np.max(np.reshape(alt, (365*4+366, 24)), axis=1), columns=['max_alt'], index=DD.index)
        x_nut = pd.concat((DD, solar), axis=1)
        y_nut = predictor[profile_type].predict(x_nut.values)
        y_nut = pd.DataFrame(y_nut.flatten(), columns=['value'], index=pd.date_range(start=datetime.datetime(2015, 1, 1), periods=43824, freq='60min'))
        y_nut.index.name = 'weather_datetime'
        y_nut['gau'] = location['NUTS_ID'].lower()
        y_nut = y_nut.set_index(['gau'], append=True)
        y_nut[np.tile((DD['CDD' if h_or_c == 'Cooling' else 'HDD'] == 0).values, [24,1]).T.flatten()] = 0
        data.append(y_nut)

    fill = y_nut.copy()
    for missing_gau in set(spatial_join['nuts1'].unique()) - set([cor.lower() for cor in coord['NUTS_ID']]):
        fill = fill.reset_index()
        fill['gau'] = missing_gau
        fill = fill.set_index(['weather_datetime', 'gau'])
        data.append(fill)
    result = pd.concat(data)

    # result['final_energy'] = 'electricity'
    # # result['final_energy'] = 'rest'

    result.to_csv(os.path.join('C:\github\ep_db_eu\database\ShapeData', 'commercial_heat_pump.csv.gz'.format(profile_type)), compression='gzip')