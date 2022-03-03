import os
import pandas as pd
import json

# Finds root directory of user
ROOT_DIR = os.path.dirname(os.path.abspath((__file__)))

''' Here we collect the data for three of the top 'proper' cryptocurrencies on the market (Bitcoin, Ethereum, Solana) '''

''' Bitcoin '''
# All five raw BTC data filepaths
BTC_MarToApr = '/../data/cryptocurrencies/raw/BTC(1)_MarToApr.json'
BTC_AprToJun = '/../data/cryptocurrencies/raw/BTC(2)_AprToJun.json'
BTC_JunToSep = '/../data/cryptocurrencies/raw/BTC(3)_JunToSep.json'
BTC_SepToDec = '/../data/cryptocurrencies/raw/BTC(4)_SepToDec.json'
BTC_DecToMar = '/../data/cryptocurrencies/raw/BTC(5)_DecToMar.json'

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


''' Ethereum '''
# All five raw ETH data filepaths
ETH_MarToApr = '/../data/cryptocurrencies/raw/ETH(1)_MarToApr.json'
ETH_AprToJun = '/../data/cryptocurrencies/raw/ETH(2)_AprToJun.json'
ETH_JunToSep = '/../data/cryptocurrencies/raw/ETH(3)_JunToSep.json'
ETH_SepToDec = '/../data/cryptocurrencies/raw/ETH(4)_SepToDec.json'
ETH_DecToMar = '/../data/cryptocurrencies/raw/ETH(5)_DecToMar.json'

# ETH records collected and merged
file = open(ROOT_DIR + ETH_MarToApr, 'r')
eth_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + ETH_AprToJun, 'r')
eth_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + ETH_JunToSep, 'r')
eth_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + ETH_SepToDec, 'r')
eth_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + ETH_DecToMar, 'r')
eth_data_5 = json.load(file)
file.close()
eth_data = eth_data_1['Data']['Data'] + eth_data_2['Data']['Data'] + eth_data_3['Data']['Data'] \
        + eth_data_4['Data']['Data'] + eth_data_5['Data']['Data']
eth_df = pd.DataFrame.from_records(eth_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])

''' Solana '''
# All five raw SOL data filepaths
SOL_MarToApr = '/../data/cryptocurrencies/raw/SOL(1)_MarToApr.json'
SOL_AprToJun = '/../data/cryptocurrencies/raw/SOL(2)_AprToJun.json'
SOL_JunToSep = '/../data/cryptocurrencies/raw/SOL(3)_JunToSep.json'
SOL_SepToDec = '/../data/cryptocurrencies/raw/SOL(4)_SepToDec.json'
SOL_DecToMar = '/../data/cryptocurrencies/raw/SOL(5)_DecToMar.json'

# SOL records collected and merged
file = open(ROOT_DIR + SOL_MarToApr, 'r')
sol_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + SOL_AprToJun, 'r')
sol_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + SOL_JunToSep, 'r')
sol_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + SOL_SepToDec, 'r')
sol_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + SOL_DecToMar, 'r')
sol_data_5 = json.load(file)
file.close()
sol_data = sol_data_1['Data']['Data'] + sol_data_2['Data']['Data'] + sol_data_3['Data']['Data'] \
        + sol_data_4['Data']['Data'] + sol_data_5['Data']['Data']
sol_df = pd.DataFrame.from_records(sol_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])


# Each proper coin converted to a dataframe with selected columns
btc_df = pd.DataFrame.from_records(btc_data, columns=['time', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
eth_df = pd.DataFrame.from_records(eth_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
sol_df = pd.DataFrame.from_records(sol_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])

# Convert UNIX timestamp unit to date unit
btc_df['time'] = pd.to_datetime(btc_df['time'],unit='s')

# Add proper coin label to column names for dataframe merge
btc_df.rename(columns={'high': 'btc_high', 'low': 'btc_low', 'open': 'btc_open', 'volumefrom': 'btc_volumefrom', \
    'volumeto': 'btc_volumeto', 'close': 'btc_close'}, inplace=True)
eth_df.rename(columns={'high': 'eth_high', 'low': 'eth_low', 'open': 'eth_open', 'volumefrom': 'eth_volumefrom', \
    'volumeto': 'eth_volumeto', 'close': 'eth_close'}, inplace=True)
sol_df.rename(columns={'high': 'sol_high', 'low': 'sol_low', 'open': 'sol_open', 'volumefrom': 'sol_volumefrom', \
    'volumeto': 'sol_volumeto', 'close': 'sol_close'}, inplace=True)

# Merge the dataframes
proper_coin_df = btc_df.join([eth_df, sol_df])

# Check that data is clean (missing entries, NaN in df)
if proper_coin_df.isnull().values.any():
    print("Null entry found in proper coin dataframe.")

# Save final meme coin dataframe to csv file
proper_coin_df.to_csv(ROOT_DIR + '/../data/cryptocurrencies/cleaned/proper_coin_data.csv')



''' Here we collect the data for three of the top 'meme' cryptocurrencies on the market (Dogecoin, Shiba Inu, Sushi) '''

''' Dogecoin '''
# All five raw DOGE data filepaths are defined here
DOGE_MarToApr = '/../data/cryptocurrencies/raw/DOGE(1)_MarToApr.json'
DOGE_AprToJun = '/../data/cryptocurrencies/raw/DOGE(2)_AprToJun.json'
DOGE_JunToSep = '/../data/cryptocurrencies/raw/DOGE(3)_JunToSep.json'
DOGE_SepToDec = '/../data/cryptocurrencies/raw/DOGE(4)_SepToDec.json'
DOGE_DecToMar = '/../data/cryptocurrencies/raw/DOGE(5)_DecToMar.json'

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


''' Shiba Inu '''
# All five raw SHIB data filepaths are defined here
SHIB_MarToApr = '/../data/cryptocurrencies/raw/SHIB(1)_MarToApr.json'
SHIB_AprToJun = '/../data/cryptocurrencies/raw/SHIB(2)_AprToJun.json'
SHIB_JunToSep = '/../data/cryptocurrencies/raw/SHIB(3)_JunToSep.json'
SHIB_SepToDec = '/../data/cryptocurrencies/raw/SHIB(4)_SepToDec.json'
SHIB_DecToMar = '/../data/cryptocurrencies/raw/SHIB(5)_DecToMar.json'

# SHIB records collected and merged
file = open(ROOT_DIR + SHIB_MarToApr, 'r')
shib_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + SHIB_AprToJun, 'r')
shib_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + SHIB_JunToSep, 'r')
shib_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + SHIB_SepToDec, 'r')
shib_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + SHIB_DecToMar, 'r')
shib_data_5 = json.load(file)
file.close()
shib_data = shib_data_1['Data']['Data'] + shib_data_2['Data']['Data'] + shib_data_3['Data']['Data'] \
        + shib_data_4['Data']['Data'] + shib_data_5['Data']['Data']


''' Sushi '''
# All five raw SUSHI data filepaths are defined here
SUSHI_MarToApr = '/../data/cryptocurrencies/raw/SUSHI(1)_MarToApr.json'
SUSHI_AprToJun = '/../data/cryptocurrencies/raw/SUSHI(2)_AprToJun.json'
SUSHI_JunToSep = '/../data/cryptocurrencies/raw/SUSHI(3)_JunToSep.json'
SUSHI_SepToDec = '/../data/cryptocurrencies/raw/SUSHI(4)_SepToDec.json'
SUSHI_DecToMar = '/../data/cryptocurrencies/raw/SUSHI(5)_DecToMar.json'

# SUSHI records collected and merged
file = open(ROOT_DIR + SUSHI_MarToApr, 'r')
sushi_data_1 = json.load(file)
file.close()
file = open(ROOT_DIR + SUSHI_AprToJun, 'r')
sushi_data_2 = json.load(file)
file.close()
file = open(ROOT_DIR + SUSHI_JunToSep, 'r')
sushi_data_3 = json.load(file)
file.close()
file = open(ROOT_DIR + SUSHI_SepToDec, 'r')
sushi_data_4 = json.load(file)
file.close()
file = open(ROOT_DIR + SUSHI_DecToMar, 'r')
sushi_data_5 = json.load(file)
file.close()
sushi_data = sushi_data_1['Data']['Data'] + sushi_data_2['Data']['Data'] + sushi_data_3['Data']['Data'] \
        + sushi_data_4['Data']['Data'] + sushi_data_5['Data']['Data']
 
# Each memecoin converted to a dataframe with selected columns
doge_df = pd.DataFrame.from_records(doge_data, columns=['time', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
shib_df = pd.DataFrame.from_records(shib_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])
sushi_df = pd.DataFrame.from_records(sushi_data, columns=['high', 'low', 'open', 'volumefrom', 'volumeto', 'close'])

# Convert UNIX timestamp unit to date unit
doge_df['time'] = pd.to_datetime(btc_df['time'],unit='s')

# Add memecoin label to column names for dataframe merge
doge_df.rename(columns={'high': 'doge_high', 'low': 'doge_low', 'open': 'doge_open', 'volumefrom': 'doge_volumefrom', \
    'volumeto': 'doge_volumeto', 'close': 'doge_close'}, inplace=True)
shib_df.rename(columns={'high': 'shib_high', 'low': 'shib_low', 'open': 'shib_open', 'volumefrom': 'shib_volumefrom', \
    'volumeto': 'shib_volumeto', 'close': 'shib_close'}, inplace=True)
sushi_df.rename(columns={'high': 'sushi_high', 'low': 'sushi_low', 'open': 'sushi_open', 'volumefrom': 'sushi_volumefrom', \
    'volumeto': 'sushi_volumeto', 'close': 'sushi_close'}, inplace=True)

# Merge the dataframes
meme_coin_df = doge_df.join([shib_df, sushi_df])

# Check that data is clean (missing entries, NaN in df)
if meme_coin_df.isnull().values.any():
    print("Null entry found in meme coin dataframe.")

# Save final meme coin dataframe to csv file
meme_coin_df.to_csv(ROOT_DIR + '/../data/cryptocurrencies/cleaned/meme_coin_data.csv')

''' Samples created here for Data Deliverable '''
proper_coin_df.head(100).to_csv(ROOT_DIR + '/../data/cryptocurrencies/sample/proper_coin_sample.csv')
meme_coin_df.head(100).to_csv(ROOT_DIR + '/../data/cryptocurrencies/sample/meme_coin_sample.csv')