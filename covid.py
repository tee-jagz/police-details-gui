import pandas as pd

df = pd.read_csv('data/specimenDate_ageDemographic-unstacked.csv')
# df = df.groupby('areaName').head(3)
# Processing data
df.date = pd.to_datetime(df.date)


# Unpivot Data
df = df.melt(id_vars=['areaType', 'areaCode', 'areaName', 'date'],
             var_name='specimenbyage', value_name='cases')

df[['rate', 'agegroup']] = df['specimenbyage'].str.split('-', expand=True)

df['agegroup'] = df['agegroup'].str.replace('_', '-', regex=True)
df = df[df.agegroup != 'unassigned']
df = df.drop('specimenbyage', axis=1)
df["rate"].replace({"newCasesBySpecimenDate": "Daily",
                    "newCasesBySpecimenDateRollingRate": "Rolling Avg",
                    "newCasesBySpecimenDateRollingSum": "Cummulative"},
                   inplace=True)
df["areaType"].replace({"overview": "UK", "region": "Region",
                        "ltla": "LTLA",
                        "utla": "UTLA"}, inplace=True)
# df = df.sort_values(by=[ 'areaName', 'date'])
df = df.set_index(['areaType', 'areaCode', 'areaName', 'date',  'rate',
                   'agegroup'])['cases'].unstack().reset_index()

df['total'] = df[['0-4', '0-59',
                  '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
                  '40-44', '45-49', '5-9', '50-54', '55-59', '60-64',
                  '65-69', '70-74', '75-79', '80-84', '85-89', '90+']].sum(
                                                        axis=1)

areaType = sorted(list(set(df.areaType)))
areaType.remove('nation')
areaName = sorted(list(set(df.areaName)))
areaCode = sorted(list(set(df.areaCode)))
rate = sorted(list(set(df.rate)))
dates = sorted(list(set(df.date)))
