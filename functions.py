
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

    References:
    ----------
    [1] Martingale. Encyclopedia of Mathematics. URL: http://encyclopediaofmath.org/index.php?title=Martingale&oldid=49256
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



def roll_model(data) -> dict:
    ''' 
    Function which principal objective is to calculate observed bid and ask as well as
    the theorical ones
    
    # Arguments:
    
    data: order books in a dictionary type

    # Returns:

    returns a dictionary which contains theorical ask and bid as well as the observed ones and 
    it also returns a theorical spread

    # References:
    - 'El modelo de Roll' pdf by Juan Francisco Muñoz-Elguezbal (July 18, 2017)

    '''

    ob_data = dt.data
    ob_ts = list(ob_data.keys())
    prices = [(ob_data[ob_ts[i]]['ask'][0] + ob_data[ob_ts[i]]['bid'][0])*.5 for i in range(0, len(ob_ts))]

    observed_ask = []
    observed_bid = []
    for ob_i in range(len(ob_ts)):
        observed_ask.append(ob_data[ob_ts[ob_i]]['ask']['0'])
        observed_bid.append(ob_data[ob_ts[ob_i]]['bid']['0'])

    dif = []
    for i in range(len(ob_ts)-1):
        dif.append(prices[i+1] - prices[i])


    variance = np.cov(dif[1:len(dif)-1],dif[2:])[1][1]
    covariance = np.cov(dif[1:len(dif)-1],dif[2:])[1][0]


    Roll_Model_Spread = 2*(np.sqrt(-covariance))

    theorical_ask = []
    theorical_bid = []
    for mid_price in prices:
        theorical_ask.append(mid_price + Roll_Model_Spread)
        theorical_bid.append(mid_price - Roll_Model_Spread)

    roll_model_info = {'Roll_Model_Spread':Roll_Model_Spread,'observed_ask':observed_ask,'observed_bid':observed_bid,'theorical_ask':theorical_ask,'theorical_bid':theorical_bid,
    'Final_Parameters':[variance,covariance]}
   
    return roll_model_info