import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Covid:
    def __init__(self):
        self.adr = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
        self.adr_cnf = self.adr + 'time_series_covid19_confirmed_global.csv'
        self.adr_dth = self.adr + 'time_series_covid19_deaths_global.csv'
        self.adr_rcv = self.adr + 'time_series_covid19_recovered_global.csv'

    def _read_regions(self, url):
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
        daily = df.diff().dropna().astype(int)
        return daily

    def _read_countries(self, url):
        df = pd.read_csv(url).drop(['Province/State', 'Lat', 'Long'], axis=1)
        df = df.groupby('Country/Region').sum().T
        df.index = pd.to_datetime(df.index)
        daily = df.diff().dropna().astype(int)
        return daily

    def confirmed(self, by_country=True):
        if by_country:
            return self._read_countries(self.adr_cnf)
        else:
            return self._read_regions(self.adr_cnf)

    def death(self, by_country=True):
        if by_country:
            return self._read_countries(self.adr_dth)
        else:
            return self._read_regions(self.adr_dth)

    def recovered(self, by_country=True):
        if by_country:
            return self._read_countries(self.adr_rcv)
        else:
            return self._read_regions(self.adr_rcv)
