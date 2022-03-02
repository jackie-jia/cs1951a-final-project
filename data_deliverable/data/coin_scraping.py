''' This file retrieves one year of hour to hour Bitcoin and Dogecoin data from the CryptoCompare API '''

import requests
import pandas as pd
import json

# Key ready to append to CryptoCompare link
API_key = '&api_key=b7c3016be1c1ed1846f62faf8c67b93b05ef0ec4122a489cda37945114a3e8b1'

''' 
Due to the limit of 2000 hours of historical data per request, the year is separated into five intervals. The toTs
URL parameter sets the endpoint of the interval request, expressed by a UNIX Timestamp. The conversion from dates to
UNIX timestamps were made using this website: https://www.epochconverter.com. The data is from 12:00 AM on March 1st 
2021 to 12:00 AM on March 1st 2022.
'''

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
with open('BTC(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(BTC_AprToJun + API_key)
r = r.json()
with open('BTC(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(BTC_JunToSep + API_key)
r = r.json()
with open('BTC(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(BTC_SepToDec + API_key)
r = r.json()
with open('BTC(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(BTC_DecToMar + API_key)
r = r.json()
with open('BTC(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)

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
with open('DOGE(1)_MarToApr.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 2: Thursday, April 1, 2021 (1:00:00 PM) - Wednesday, June 23, 2021 (10:00:00 PM)
r = requests.get(DOGE_AprToJun + API_key)
r = r.json()
with open('DOGE(2)_AprToJun.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 3: Wednesday, June 23, 2021 (3:00:00 PM) - Wednesday, September 15, 2021 (7:00:00 AM)
r = requests.get(DOGE_JunToSep + API_key)
r = r.json()
with open('DOGE(3)_JunToSep.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 4: Wednesday, September 15, 2021 (7:00:00 AM) - Tuesday, December 7, 2021 (3:00:00 PM)
r = requests.get(DOGE_SepToDec + API_key)
r = r.json()
with open('DOGE(4)_SepToDec.json','w') as json_file:
    json.dump(r,json_file)

# REQUEST 5: Tuesday December 7 2021 (3:00:00 PM) - Tuesday March 1 2022 (12:00:00 AM)
r = requests.get(DOGE_DecToMar + API_key)
r = r.json()
with open('DOGE(5)_DecToMar.json','w') as json_file:
    json.dump(r,json_file)








