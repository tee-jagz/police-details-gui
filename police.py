import requests as re
import calendar
from collections import Counter
import pandas as pd
import datetime


def do(request='Default'):
    if request == 'Default':
        response = re.get('https://data.police.uk/api/forces')
        jresp = response.json()

        force = dict()
        for i in jresp:
            force[i['name']] = i['id']
        return force


def fplot(month, year, force, info=None):
    month = list(calendar.month_name).index(month)

    forcep = do()
    url = f'https://data.police.uk/api/stops-no-location?force={forcep[force]}&date={year}-{month}'
    dat = re.get(url).json()
    rec = []
    if info == 'Age':
        for i in dat:
            rec.append(str(i['age_range']))
        
    elif info == 'Gender':
        for i in dat:
            rec.append(str(i['gender']))
    elif info == 'Ethnic':
        for i in dat:
            data = str(i['self_defined_ethnicity'])
            dat = (data[:10] + '..') if len(data) > 10 else data
            rec.append(dat)
    elif info == 'Stop Purpose':
        for i in dat:
            data = str(i['object_of_search'])
            dat = (data[:10] + '..') if len(data) > 10 else data
            rec.append(dat)
    elif info == 'Outcome':
        for i in dat:
            data = str(i['outcome'])
            dat = (data[:10] + '..') if len(data) > 10 else data
            rec.append(dat)
    return dict(Counter(rec))


def cplot(fmon, fyear, tmon, tyear, pol, fil):
    tmon = list(calendar.month_name).index(tmon)
    fmon = list(calendar.month_name).index(fmon)
    forcep = do()
    df = pd.DataFrame(columns=['Date', 'Par'])
    # startDate = datetime(2020, fmon, 1)
    # endDate = datetime(2020, tmon, )
  
    # # stores 31 days that can be added
    # addDays = datetime.timedelta(month=1)
    while fyear <= tyear:
        if fyear > tyear:
            print('check0')
            break
        elif (fmon > tmon) & (fyear == tyear):
            print('check1')
            break
        print('Loading...')
        url = f'https://data.police.uk/api/stops-no-location?force={forcep[pol]}&date={fyear}-{fmon}'
        dat = re.get(url).json()
        monv = f'{calendar.month_abbr[fmon]}-{fyear}'
        if fil == 'Age':
            filt = 'age_range'
        elif fil == 'Gender':
            filt = 'gender'
        elif fil == 'Ethnic':
            filt = 'self_defined_ethnicity'
        elif fil == 'Stop Purpose':
            filt = 'object_of_search'
        elif fil == 'Outcome':
            filt = 'outcome'
        for n in dat:
            df.loc[len(df)] = [monv, str(n[filt])]

        if fmon % 12 == 0:
            fmon = 1
            fyear += 1
        else:
            fmon += 1
        # startDate += addDays

    d = df.groupby(['Date', 'Par'])['Par'].count().to_frame(name='Count').reset_index()
    #d.Date = d.Date.astype(str)
    return d
