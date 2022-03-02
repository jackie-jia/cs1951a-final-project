from bs4 import BeautifulSoup
import requests
import sqlite3
import urllib
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

API_key = '&api_key=b7c3016be1c1ed1846f62faf8c67b93b05ef0ec4122a489cda37945114a3e8b1'
# CryptoCompare_URL_first = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=1'
# CryptoCompare_URL_second = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=1&toTs=1635818413'
# Shiba_Ten_Hours = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=SHIB&tsym=USD&limit=9&toTs=1614646800'
# r = requests.get(Shiba_Ten_Hours + API_key)
# r = r.json()
# print('Shiba Data')
# print(r['Data'])



BTC_MarToApr = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=756&toTs=1617296400'
BTC_AprToJun = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1624500000'
BTC_JunToSep = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1631703600'
BTC_SepToDec = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1638907200'
BTC_DecToMar = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000&toTs=1646110800'

# REQUESET 1: March 1, 2021 - April 1, 2021 (1:00:00 PM)
r = requests.get(BTC_MarToApr + API_key)
r = r.json()
with open('BTC_MarToApr(1).json','w') as json_file:
    json.dump(r,json_file)

# # REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
# r = requests.get(BTC_AprToJun + API_key)
# r = r.json()
# with open('BTC_AprToJun(2).json','w') as json_file:
#     json.dump(r,json_file)

# # REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
# r = requests.get(BTC_JunToSep + API_key)
# r = r.json()
# with open('BTC_JunToSep(3).json','w') as json_file:
#     json.dump(r,json_file)

# # REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
# r = requests.get(BTC_SepToDec + API_key)
# r = r.json()
# with open('BTC_SepToDec(4).json','w') as json_file:
#     json.dump(r,json_file)

# # REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
# r = requests.get(BTC_DecToMar + API_key)
# r = r.json()
# with open('BTC_DecToMar(5).json','w') as json_file:
#     json.dump(r,json_file)









