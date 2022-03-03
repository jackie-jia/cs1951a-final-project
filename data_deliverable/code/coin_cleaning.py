''' This file cleans and combines the raw coin data using a pandas dataframe '''
import os
import pandas as pd
import json

# Finds root directory of user
ROOT_DIR = os.path.dirname(os.path.abspath((__file__)))

# All five raw BTC data filepaths
BTC_MarToApr = '/../data/raw/BTC(1)_MarToApr.json'
BTC_AprToJun = '/../data/raw/BTC(2)_AprToJun.json'
BTC_JunToSep = '/../data/raw/BTC(3)_JunToSep.json'
BTC_SepToDec = '/../data/raw/BTC(4)_SepToDec.json'
BTC_DecToMar = '/../data/raw/BTC(5)_DecToMar.json'

# BTC records collected and merged
file = open(ROOT_DIR + BTC_MarToApr, 'r')
btc_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + BTC_AprToJun, 'r')
btc_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + BTC_JunToSep, 'r')
btc_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + BTC_SepToDec, 'r')
btc_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + BTC_DecToMar, 'r')
btc_data_5 = json.load(file)
file.close()
btc_data = btc_data_1['Data']['Data'] + btc_data_2['Data']['Data'] + btc_data_3['Data']['Data'] \
        + btc_data_4['Data']['Data'] + btc_data_5['Data']['Data']
btc_df = pd.DataFrame.from_records(btc_data, columns=['time', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])

# All five raw DOGE data filepaths are defined here
DOGE_MarToApr = '/../data/raw/DOGE(1)_MarToApr.json'
DOGE_AprToJun = '/../data/raw/DOGE(2)_AprToJun.json'
DOGE_JunToSep = '/../data/raw/DOGE(3)_JunToSep.json'
DOGE_SepToDec = '/../data/raw/DOGE(4)_SepToDec.json'
DOGE_DecToMar = '/../data/raw/DOGE(5)_DecToMar.json'

# DOGE records collected and merged
file = open(ROOT_DIR + DOGE_MarToApr, 'r')
doge_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + DOGE_AprToJun, 'r')
doge_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + DOGE_JunToSep, 'r')
doge_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + DOGE_SepToDec, 'r')
doge_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + DOGE_DecToMar, 'r')
doge_data_5 = json.load(file)
file.close()
doge_data = doge_data_1['Data']['Data'] + doge_data_2['Data']['Data'] + doge_data_3['Data']['Data'] \
        + doge_data_4['Data']['Data'] + doge_data_5['Data']['Data']
 
# BTC and DOGE data converted to a dataframe with selected columns (size: 8761x7)
btc_df = pd.DataFrame.from_records(btc_data, columns=['time', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
doge_df = pd.DataFrame.from_records(doge_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])

# Convert UNIX timestamp unit to date unit
btc_df['time'] = pd.to_datetime(btc_df['time'],unit='s')

# Add crytpocurrency label to column names for dataframe merge
btc_df.rename(columns={'high': 'btc_high', 'low': 'btc_low', 'open': 'btc_open', 'volumefrom': 'btc_volumefrom', \
    'volumeto': 'btc_volumeto', 'close': 'btc_close'}, inplace=True)
doge_df.rename(columns={'high': 'doge_high', 'low': 'doge_low', 'open': 'doge_open', 'volumefrom': 'doge_volumefrom', \
    'volumeto': 'doge_volumeto', 'close': 'doge_close'}, inplace=True)

# Merge the dataframes
coin_df = btc_df.join(doge_df)

# Check that data is clean (missing entries, NaN in df)
if coin_df.isnull().values.any():
    print("Null entry found in coin dataframe.")

# Save final dataframe of coin data to json file
coin_json = coin_df.to_json()
with open(ROOT_DIR + '/../data/coin_data.json','w') as file:
    json.dump(coin_json, file)