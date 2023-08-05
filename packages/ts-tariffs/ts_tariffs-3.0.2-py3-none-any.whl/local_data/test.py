from datetime import timedelta
from typing import List
import pandas as pd

from local_data.test_tariffs import tariff_data
from ts_tariffs.meters import MeterData, Meters
from ts_tariffs.billing import TariffRegime

df = pd.read_csv('C:/Users/114261/Dropbox (UTS ISF)/1. 2021 Projects/21090_RACE_RACE Abattoirs - Fast Track/4. Work in progress/modelling/data_wrangling/JBS_elec_clean.csv')
start_date = '2021-07-01'
end_date = '2021-07-31'
df['datetime'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
df.set_index('datetime', inplace=True)
df = df.loc[start_date: end_date]

sample_rate = timedelta(hours=0.5)
meters = Meters({
    'energy': MeterData('energy', df['Consumption (kWh)'], timedelta(hours=0.5), units='kWh'),
    'apparent_power': MeterData('apparent_power', df['Demand (KVA)'], timedelta(hours=0.5), units='kVA'),
    'real_power': MeterData('real_power', df['demand_power'], timedelta(hours=0.5), units='kW'),
})

tariffs = TariffRegime(tariff_data)

bill = tariffs.calculate_bill(name='example', meters=meters)
print(bill.as_series)
