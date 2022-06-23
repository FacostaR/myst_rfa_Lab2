
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LABORATORY 2: High-Frequency Models                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: FacostaR                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/FacostaR/myst_rfa_Lab2                                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import data as dt
import pandas as pd

# ============================================FUNCIONES======================================== #
def experiments(ob_data: dict, ob_ts: list, method: str) -> pd.DataFrame:
    """
    Function used to perform experiments with orderbook data.

    arguments:
    ----------
    ob_data: dictionary
    dictionary type with the following structure:
    'timestamp'
    'bid_size'
    'bid'
    'ask'
    'ask_size'

    ob_ts: list
    list with timestamps in string format.

    method: str: 'midprice' or 'wmidprice'
    string with the method that's going to be used in calculations.

    Returns -> dataframe 
    """

    l_ts = [pd.to_datetime(i) for i in ob_ts]
    minutes = [i.minute for i in l_ts]

    m_counter = {i: minutes.count(i) for i in set(minutes)}

    dict = {'time': ob_ts, 'minutes': minutes}
    res = pd.DataFrame(data = dict)
    res = res.sort_values(by=['minutes', 'time'])
    res = res.reset_index(drop=True)

    if method == 'midprice':
        prices = [(ob_data[ob_ts[i]]['ask'][0] + ob_data[ob_ts[i]]['bid'][0])*.5 for i in range(0, len(ob_ts))]

    elif method == 'wmidprice':
        fwmp = lambda x: np.sum((x['ask_size']/np.sum([x['bid_size'], x['ask_size']]))*x['bid'] + (x['bid_size']/np.sum([x['bid_size'], x['ask_size']]))*x['ask'])
        prices = np.round([fwmp(ob_data[ob_ts[i]]) for i in range(len(ob_ts))], 2)
    else:
        print('error, method should be: \"midprice\" or  \"wmidprice\"')

    res.drop(index=res.index[0], axis=0, inplace=True)
    res = res.reset_index(drop=True)

    res['martingale'] = [prices[i+1] == prices[i] for i in range(len(prices)-1)]
    by_minute = res.groupby('minutes')

    x = pd.DataFrame(by_minute['martingale'].sum())

    e1 = list(x['martingale'])
    total = [m_counter[i] for i in range(len(m_counter))]
    prop1 = np.round([e1[i]/total[i] for i in range(len(total))], 4)
    e2 = np.round([total[i]-e1[i] for i in range(len(total))], 4)
    prop2 = np.round([e2[i]/total[i] for i in range(len(total))], 4)

    exp = pd.DataFrame({'intervalo': list(np.arange(0, 60)), 'total': total, 
        'e1': e1, 'e1_proportion': prop1,
        'e2': e2, 'e2_proportion': prop2})
    return exp
