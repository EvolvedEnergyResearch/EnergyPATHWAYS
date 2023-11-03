from degreedays.api import DegreeDaysApi, AccountKey, SecurityKey
from degreedays.api.data import DataSpec, Calculation, Temperature, DatedBreakdown, Period, Location, DataSpecs, LocationDataRequest
from degreedays.time import DayRange, DayRanges, DayOfWeek, StartOfMonth, StartOfYear
from degreedays.geo import LongLat
from degreedays.api import RateLimitError
from datetime import date
import pandas as pd
import os
import time

# https://www.degreedays.net/api/integration

api = DegreeDaysApi.fromKeys(
        AccountKey("ju4y-jy4q-2n3w"),
        SecurityKey("54sw-pd4k-m346-gxfg-fcf6-xdfd-zf8f-662v-gynd-wbrz-txyq-pbxq-6wdf"))

period = DatedBreakdown.daily(Period.dayRange(DayRange(date(2000, 1, 1), date(2019, 12, 31)),
                                              minimumDayRangeOrNone=DayRange(date(2000, 1, 1), date(2019, 12, 31))))


def dd_lookup(lat, long, type):
    if type.lower() == 'hdd':
        ddSpec = DataSpec.dated(Calculation.heatingDegreeDays(Temperature.fahrenheit(65)), period)
    elif type.lower() == 'cdd':
        ddSpec = DataSpec.dated(Calculation.coolingDegreeDays(Temperature.fahrenheit(65)), period)
    else:
        raise ValueError("type {} not recognized".format(type))
    location = Location.longLat(LongLat(long, lat))
    request = LocationDataRequest(location, DataSpecs(ddSpec))

    errors = 0
    while True:
        try:
            response = api.dataApi.getLocationData(request)
            break
        except RateLimitError:
            errors += 1
            if errors>5:
                raise
            print('sleeping {} seconds'.format(20 * 60))
            time.sleep(20*60)

    hddData = response.dataSets[ddSpec]
    columns = ['hdd65'] if type.lower() == 'hdd' else ['cdd65']
    df = pd.DataFrame([day.value for day in hddData.values], index=pd.Index([day.firstDay for day in hddData.values], name='date'), columns=columns)
    return df


coord = pd.read_csv(r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\Geographies\shapefile\nuts1_coord.csv')
coord = coord[['NUTS_ID', 'long', 'lat']]

base_dir = r'D:\Dropbox (EER)\Evolved Energy Research\Projects & Marketing\Third Way\Decarb Europe\Work Files\End-use Load Profiles\hdd_cdd_regression'

for i, (nuts_id, long, lat) in coord.iterrows():
    if nuts_id+'.csv' not in os.listdir(os.path.join(base_dir, 'cdd')):
        dd_df = dd_lookup(lat, long, 'cdd')
        dd_df.to_csv(os.path.join(base_dir, 'cdd', nuts_id+'.csv'))
        print("{} cdd download success".format(nuts_id))
    else:
        print("{} cdd already downloaded... skipping".format(nuts_id))

    if nuts_id+'.csv' not in os.listdir(os.path.join(base_dir, 'hdd')):
        dd_df = dd_lookup(lat, long, 'hdd')
        dd_df.to_csv(os.path.join(base_dir, 'hdd', nuts_id+'.csv'))
        print("{} hdd download success".format(nuts_id))
    else:
        print("{} hdd already downloaded... skipping".format(nuts_id))

    time.sleep(2)