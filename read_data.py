import pandas as pd


adr = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'

adr_cnf = adr + 'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
adr_dth = adr + 'csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
adr_rcv = adr + 'csse_covid_19_time_series/time_series_covid19_recovered_global.csv'


def read_regions(url):
    '''Read time series df and return daily df'''
    df = pd.read_csv(url).drop(['Lat', 'Long'], axis=1)
    df['Province/State'] = df['Province/State'].fillna('')
    df['region'] = df['Country/Region'] + '_' + df['Province/State']
    df = df.drop(['Country/Region', 'Province/State'], axis=1)
    cols = ['region'] + list(df.columns[:-1])
    df = df[cols]
    df = df.set_index('region')
    df = df.T
    df.index = pd.to_datetime(df.index)
    daily = df.diff()
    return daily

def read_countries(url):
    df = pd.read_csv(adr_dth).drop(['Province/State', 'Lat', 'Long'], axis=1)
    df = df.groupby('Country/Region').sum().T
    df.index = pd.to_datetime(df.index)
    daily = df.diff()
    return daily
    

# Reading deaths
dth = read_countries(adr_dth)

