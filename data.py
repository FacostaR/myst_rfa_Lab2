
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LABORATORY 2: High-Frequency Models                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: FacostaR                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/FacostaR/myst_rfa_Lab2                                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import json
import pandas as pd

# Orderbooks JSON file
f = open('files/orderbooks_05jul21.json')

# Return JSON pbject as a dictionary
orderbooks_data = json.load(f)
data = orderbooks_data['bitfinex']

# Drop None keys
data = {i_key: i_value for i_key, i_value in data.items() if i_value is not None}

# Convert to dataframe and rearange colums
data = {i_ob: pd.DataFrame(data[i_ob])[['bid_size', 'bid', 'ask', 'ask_size']]
           if data[i_ob] is not None else None for i_ob in list(data.keys())}
# data
ts = list(data.keys())
l_ts = [pd.to_datetime(i_ts) for i_ts in ts]