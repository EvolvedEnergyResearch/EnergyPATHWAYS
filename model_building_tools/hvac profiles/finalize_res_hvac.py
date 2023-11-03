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
from sklearn.linear_model import LinearRegression
import time
import ephem
import pdb
from fuzzywuzzy import process
import seaborn as sns; sns.set()
from energyPATHWAYS import util
from pandas.tseries.holiday import get_calendar
import pytz
import datetime as DT

directory = r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Annual Refresh\pre 2020\Pathways\shape data\v2'
weather_locations = pd.read_csv(os.path.join(directory, 'process_solar_profiles', 'TMY3_StationsMeta.csv'), index_col=0)

cooling_degree_days_TMY3 = pd.read_csv(os.path.join(directory, 'weather data', 'cooling_degree_days_TMY3.csv'))
heating_degree_days_TMY3 = pd.read_csv(os.path.join(directory, 'weather data', 'heating_degree_days_TMY3.csv'))

heat_pump_cop_curve = pd.read_csv(os.path.join(directory, 'weather data', '2020-07_heat_pump_cop_curve_low-tech.csv'), index_col=0)
# heat_pump_cop_curve = pd.read_csv(os.path.join(directory, 'weather data', '2020-07_heat_pump_cop_curve.csv'), index_col=0)

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
RESIDENTIAL HVAC
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
    df = df.iloc[1:].astype(float)
    # the supplementary heating doesn't always exist in the file
    if 'Delivered Energy|Heating Delivered (suppl.)' in df.columns:
        heating_load = df[['Delivered Energy|Heating Delivered (main)', 'Delivered Energy|Heating Delivered (suppl.)']].sum(axis=1).to_frame()
    else:
        heating_load = df[['Delivered Energy|Heating Delivered (main)']]
    temperature = df[['Weather|Outdoor Drybulb']]
    temperature_round = temperature.round()

    hourly_cop = np.array([heat_pump_cop_curve.loc[temp,'COP'].values[0] for temp in temperature_round.values])
    kwh = 1/hourly_cop*0.00029317 * heating_load.values.flatten()
    kwh = pd.DataFrame(kwh).clip(0, None, axis=1)
    
    #### special for hybrid systems
    UTILITY_FACTOR = 0.5
    sorted_heating_load = np.sort(kwh.values.flatten())
    cum_sum_heating = np.cumsum(sorted_heating_load)
    total_heating_load = cum_sum_heating[-1]
    heating_cut = np.nonzero(cum_sum_heating > total_heating_load * UTILITY_FACTOR)[0][0]
    max_electric_heating = sorted_heating_load[heating_cut]
    kwh[kwh > max_electric_heating] = 0 # when we want to get electricity
    # kwh[kwh < max_electric_heating] = 0 # when we want to get pipeline gas
    ####
    
    print( geography, kwh.max().max(), np.percentile(temperature.values.flatten()[np.nonzero(kwh.values.flatten())], .01))
    return kwh.values


def get_load_data(profile_type, geography):
    file_name = profile_types[profile_type]['file_name']+'.csv'
    prof_col = profile_types[profile_type]['profile_name']
    USAF = geographies[geography]
    profile_path = os.path.join(base_path, geography, file_name)
    temp = pd.read_csv(profile_path, index_col=False)
    temp.columns = [c.split(' - ')[1] if ' - ' in c else c for c in temp.columns]
    data = pd.DataFrame(index=pd.date_range(start=datetime.datetime(2006, 1, 1), periods=8760, freq='60min'))
    data.index.names = ['datetime']
    if profile_type=='high_efficiency_heat_pump_heating_res':
        data[geographies[geography]] = heat_pump_special_calc(temp, geography)
    else:
        data[geographies[geography]] = temp[prof_col].values[1:].astype(float)
    data['hour'] = data.index.hour
    data['date'] = data.index.date
    data['USAF'] = USAF
    data = data.set_index(['USAF', 'date', 'hour'], append=True)
    data.index = data.index.droplevel('datetime')
    data = data.squeeze().unstack('hour')
    return data

def get_moisture_type(geography):
    # A is moist, B is dry, C is marine
    code = geography.split('_')[0][-1]
    return _get_moisture_type(code)

def get_climate_number(geography):
    # A is moist, B is dry, C is marine
    number = geography.split('_')[0][0]
    return int(number)

def _get_moisture_type(code):
    if code=='A':
        return 1
    elif code=='C':
        return 2
    else:
        return 3

profile_types = {
'electric_furnace_res':                     {'file_name':'Electric_Furnace_0.99_AFUE_CentralAC_SEER_17', 'profile_name':'Site Energy|Heating (E)'},
'reference_central_ac_res':                 {'file_name':'Electric_Furnace_0.99_AFUE_CentralAC_SEER_17', 'profile_name':'Site Energy|Cooling (E)'},
'high_efficiency_central_ac_res':           {'file_name':'Electric_Furnace_0.99_AFUE_CentralAC_SEER_27', 'profile_name':'Site Energy|Cooling (E)'},
'reference_room_ac_res':                    {'file_name':'Electric_Furnace_0.99_AFUE_RoomAC_EER_9.8', 'profile_name':'Site Energy|Cooling (E)'},
'high_efficiency_room_ac_res':              {'file_name':'Electric_Furnace_0.99_AFUE_RoomAC_EER_11.5', 'profile_name':'Site Energy|Cooling (E)'},
# 'reference_heat_pump_heating_res':          {'file_name':'Air_Source_Heat_Pump_HSPF_8.2_SEER_14', 'profile_name':'Site Energy|Heating (E)'},
'high_efficiency_heat_pump_heating_res':    {'file_name':'Air_Source_Heat_Pump_HSPF_10_SEER_22', 'profile_name':'Site Energy|Heating (E)'},
# 'reference_heat_pump_cooling_res':          {'file_name':'Air_Source_Heat_Pump_HSPF_8.2_SEER_14', 'profile_name':'Site Energy|Cooling (E)'},
'high_efficiency_heat_pump_cooling_res':    {'file_name':'Air_Source_Heat_Pump_HSPF_10_SEER_22', 'profile_name':'Site Energy|Cooling (E)'},
}

geographies = {
'1A_Miami': 722020,
'2A_Houston': 722430,
'2B_Phoenix': 722780,
'3A_Atlanta': 722190,
'3B-Coast_Los Angeles': 722950,
'3B_Las Vegas': 723677,
'3C_San Francisco':724940,
'4A_Baltimore':724060,
'4B_Albuquerque':723650,
'4C_Seattle':727930,
'5A_Chicago':725300,
'5B_Boulder':724699,
'6A_Minneapolis':726580,
'6B_Helena':727720,
'7_Duluth':727450,
'8_Fairbanks':702610
}

cal = get_calendar('USFederalHolidayCalendar')  # possible to change to other holiday systems in config
train_holidays = [str(stamp.date()) for stamp in cal.holidays(start=datetime.datetime(2006, 1, 1), end=datetime.datetime(2006, 12, 31))]

base_path = os.path.join(directory, 'weather data', 'NREL_load_shapes', 'ElecHomeResults', 'ElecHomeResults', 'Hourly')

validating_size = .01

fits = {}
predictor = {}
for profile_type in profile_types:
    if profile_type!='high_efficiency_heat_pump_heating_res':
        continue
    h_or_c = profile_types[profile_type]['profile_name'].split('|')[1].split(' ')[0]

    fits[profile_type] = {}
    x = pd.DataFrame()
    y = pd.DataFrame()

    for geography in geographies:
        print( profile_type, geography, get_moisture_type(geography))
        load_data = get_load_data(profile_type, geography)
        DD = get_degree_days(geography)
        DD['dayofweek'] = DD.index.get_level_values('date').dayofweek
        DD['month'] = DD.index.get_level_values('date').month

        if h_or_c == 'Cooling':
            DD = DD[['CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'CDD mean', 'dayofweek', 'month']]
        elif h_or_c == 'Heating':
            DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'HDD mean', 'dayofweek', 'month']]

        alt, az = get_solar_angles(geography)
        solar = pd.DataFrame(np.max(np.reshape(alt, (365, 24)), axis=1), columns=['max_alt'], index=DD.index)

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
    print( '{} train = {}, validate = {}'.format(profile_type, fits[profile_type]['train'], fits[profile_type]['validate']))
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
    if profile_type!='high_efficiency_heat_pump_heating_res':
        continue
    h_or_c = profile_types[profile_type]['profile_name'].split('|')[1].split(' ')[0]
    data = []
    for i, location in coord.iterrows():
        if location['NUTS_ID'].lower() not in spatial_join['nuts1'].values:
            continue
        DD = get_degree_days_nuts(location['NUTS_ID'])
        DD['dayofweek'] = pd.DatetimeIndex(DD.index).dayofweek
        DD.loc[holidays, 'dayofweek'] = 6  # we make all of the holidays sunday
        DD['month'] = pd.DatetimeIndex(DD.index).month

        if h_or_c == 'Cooling':
            DD = DD[['CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'CDD mean', 'dayofweek', 'month']]
        elif h_or_c == 'Heating':
            DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'HDD mean', 'dayofweek', 'month']]

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

    result['final_energy'] = 'electricity'
    # result['final_energy'] = 'rest'

    result.to_csv(os.path.join('C:\github\ep_db_eu\database\ShapeData', '{}_ele.csv.gz'.format(profile_type)), compression='gzip')

# for profile_type in profile_types:
#     result = []
#     for IECC_climate_zone_state in county_to_IECC_geomap.index.get_level_values('IECC Climate Zone by state').unique():
#         geomap = util.df_slice(county_to_IECC_geomap['CDD_res_sq_ft' if h_or_c=='Cooling' else 'HDD_res_sq_ft'], IECC_climate_zone_state, 'IECC Climate Zone by state', drop_level=False, reset_index=True)
#         counties_data = []
#         for county in geomap.index.get_level_values('county'):
#             row = counties_with_climate[counties_with_climate['name']==county]
#             if len(row)!=1:
#                 pdb.set_trace()
#             row = row.T.squeeze()
#             noaa_region = row['Region ID']
#             if np.isnan(noaa_region):
#                 continue
#             print( row['name'])
#             DD = get_degree_days_noaa(noaa_region)
#             DD['moisture_type'] = _get_moisture_type(row['IECC'][-1])
#             DD['temp_zone'] = get_climate_number(row['IECC'])
#             DD['dayofweek'] = pd.DatetimeIndex(DD.index).dayofweek
#             DD.loc[holidays, 'dayofweek'] = 6  # we make all of the holidays sunday
#             DD['month'] = pd.DatetimeIndex(DD.index).month
#
#             if h_or_c == 'Cooling':
#                 DD = DD[['CDD', 'CDD 1', 'CDD -1', 'CDD -2', 'CDD mean', 'moisture_type', 'temp_zone', 'dayofweek', 'month']]
#             elif h_or_c == 'Heating':
#                 DD = DD[['HDD', 'HDD 1', 'HDD -1', 'HDD -2', 'HDD mean', 'moisture_type', 'temp_zone', 'dayofweek', 'month']]
#
#             alt, az = _get_solar_angles(lat=row['lat'], lon=row['lon'], start_date='2010/01/01 00:30:00', TZ=row['TZ'], num_hr=26304)
#             solar = pd.DataFrame(np.max(np.reshape(alt, (365*2+366, 24)), axis=1), columns=['max_alt'], index=DD.index)
#
#             x_county = pd.concat((DD, solar), axis=1)
#             y_county = regr.predict(x_county.values)
#             y_county = pd.DataFrame(y_county.flatten(), columns=['value'], index=pd.date_range(start=datetime.datetime(2010, 1, 1), periods=26304, freq='60min'))
#             y_county.index.name = 'weather_datetime'
#             y_county['county'] = row['name']
#             y_county = y_county.set_index(['county'], append=True)
#             y_county[np.tile((DD['CDD' if h_or_c == 'Cooling' else 'HDD'] == 0).values, [24,1]).T.flatten()] = 0
#             counties_data.append(y_county)
#             break
#
#         if not len(counties_data):
#             continue
#
#         counties_data = pd.concat(counties_data)
#         counties_data = util.DfOper.mult((counties_data, geomap))
#         counties_data = counties_data.groupby(level=['IECC Climate Zone by state', 'weather_datetime']).sum()
#         counties_data = counties_data.groupby(level='IECC Climate Zone by state').transform(lambda x: x / x.max())
#         counties_data = counties_data.reset_index()
#         counties_data.columns = ['gau', 'weather_datetime', 'value']
#         counties_data = counties_data.set_index(['gau', 'weather_datetime']).sort_index()
#         counties_data = counties_data.round({'value': 5})
#
#         result.append(counties_data)
#     result = pd.concat(result)
#     # this doesn't have the missing gau_ids at this point
#
#     # hawaii gets replaced with socal, alaska gets replaced with wyoming, PR with south Florida
#     for missing_gau, replicated_gau in [('Hawaii 1A', 'California 2B'), ('Alaska 7B', 'Wyoming 7A'), ('Alaska 8B', 'Wyoming 7A'), ('Puerto Rico 1A', 'Florida 1A')]:
#         replicated_slice = util.df_slice(result, [str(replicated_gau)], 'gau', drop_level=False, reset_index=True).reset_index()
#         replicated_slice['gau'] = str(missing_gau)
#         replicated_slice = replicated_slice.set_index(['gau', 'weather_datetime']).sort_index()
#         result = pd.concat((result, replicated_slice))
#
#     # result['final_energy'] = 'electricity'
#     result['final_energy'] = 'rest'
#     # result['sensitivity'] = 'high-technology'
#     # result['sensitivity'] = 'low-technology'
#
#     result.to_csv(os.path.join(directory, 'final for db import', '{}_gas.csv'.format(profile_type)))
#
# print( 'done')