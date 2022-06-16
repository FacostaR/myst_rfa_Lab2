
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import json
import numpy as np
import pandas as pd

#Open JSON file

f= open('orderbooks_05jul21.json')

# Return JSON object as a Dictionary
orderbooks_data = json.load(f)

orderbooks_data.keys()

bitfinex_ts= list(orderbooks_data['bitfinex'].keys())
kraken_ts = list(orderbooks_data['kraken'].keys())

ob_data= orderbooks_data['bitfinex']

# Drop  None Keys
ob_data= {i_key: i_value for i_key, i_value in ob_data.items() if i_value is not None}

#Convert to DataFrame and rearange columns
ob_data = {i_ob: pd.DataFrame(ob_data[i_ob])[['bid_size','bid','ask','ask_size']]
                    if ob_data[i_ob] is not None else None for i_ob in list(ob_data.keys())}

## Public Trades
pt_data= pd.read_csv('btcusdt_binance.csv', index_col='timestamp')
pt_data.index= pd.to_datetime(pt_data.index)
pt_data.rename(columns= {'amount': 'volume'}, inplace='TRUE')