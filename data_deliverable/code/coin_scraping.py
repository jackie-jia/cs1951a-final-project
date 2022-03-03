import requests
import json
import os

# Key ready to append to CryptoCompare link
API_key = '&api_key=b7c3016be1c1ed1846f62faf8c67b93b05ef0ec4122a489cda37945114a3e8b1'

# Finds root directory of user
ROOT_DIR = os.path.dirname(os.path.abspath((__file__)))

''' 
Due to the limit of 2000 hours of historical data per request, the year is separated into five intervals. The toTs
URL parameter sets the endpoint of the interval requested, expressed in the UNIX Timestamp unit. The conversion from dates to
UNIX timestamps were made using this website: https://www.epochconverter.com. The data is from 12:00 AM on March 1st 
2021 to 12:00 AM on March 1st 2022 (inclusive) for UTC-05:00 (EST), and covers three of some of the top 'proper'
cryptocurrencies (Bictoin, Ethereum, Solana) and three of some of the top 'meme' cryptocurrencies (Dogecoin, Shiba Inu,
Sushi) by market capitalization.
'''

''' Bitcoin '''
# Links for BTC (Bitcoin) historical data
BTC_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=756&toTs=1617296400'
BTC_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1624500000'
BTC_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1631703600'
BTC_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1638907200'
BTC_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for BTC data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(BTC_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/BTC(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(BTC_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/BTC(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(BTC_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/BTC(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(BTC_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/BTC(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(BTC_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/BTC(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)


''' Ethereum '''
# Links for ETH (Ethereum) historical data
ETH_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=756&toTs=1617296400'
ETH_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=2000&toTs=1624500000'
ETH_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=2000&toTs=1631703600'
ETH_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=2000&toTs=1638907200'
ETH_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for ETH data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(ETH_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/ETH(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(ETH_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/ETH(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(ETH_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/ETH(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(ETH_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/ETH(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(ETH_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/ETH(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)


''' Solana '''
# Links for SOL (Solana) historical data
SOL_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=756&toTs=1617296400'
SOL_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=2000&toTs=1624500000'
SOL_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=2000&toTs=1631703600'
SOL_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=2000&toTs=1638907200'
SOL_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for SOL data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(SOL_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SOL(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(SOL_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SOL(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(SOL_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SOL(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(SOL_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SOL(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(SOL_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SOL(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)


''' Dogecoin '''
# Links for DOGE (Dogecoin) historical data
DOGE_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=756&toTs=1617296400'
DOGE_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=2000&toTs=1624500000'
DOGE_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=2000&toTs=1631703600'
DOGE_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=2000&toTs=1638907200'
DOGE_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for DOGE data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(DOGE_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/DOGE(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(DOGE_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/DOGE(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(DOGE_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/DOGE(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(DOGE_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/DOGE(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(DOGE_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/DOGE(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)


''' Shiba Inu '''
# Links for SHIB (Shiba Inu) historical data
SHIB_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=756&toTs=1617296400'
SHIB_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=2000&toTs=1624500000'
SHIB_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=2000&toTs=1631703600'
SHIB_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=2000&toTs=1638907200'
SHIB_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for SHIB data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(SHIB_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SHIB(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(SHIB_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SHIB(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(SHIB_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SHIB(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(SHIB_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SHIB(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(SHIB_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SHIB(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)


''' Sushi '''
# Links for SUSHI (Sushi) historical data
SUSHI_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SUSHI&tsym=USD&limit=756&toTs=1617296400'
SUSHI_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SUSHI&tsym=USD&limit=2000&toTs=1624500000'
SUSHI_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SUSHI&tsym=USD&limit=2000&toTs=1631703600'
SUSHI_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SUSHI&tsym=USD&limit=2000&toTs=1638907200'
SUSHI_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SUSHI&tsym=USD&limit=2000&toTs=1646110800'

# The five requests for SUSHI data are made here, and outputted as json files
# REQUEST 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(SUSHI_MarToApr + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SUSHI(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(SUSHI_AprToJun + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SUSHI(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(SUSHI_JunToSep + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SUSHI(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(SUSHI_SepToDec + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SUSHI(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(SUSHI_DecToMar + API_key)
r = r.json()
with open(ROOT_DIR + '/../data/coin/raw/SUSHI(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)