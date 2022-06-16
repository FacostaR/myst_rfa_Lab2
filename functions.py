
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import data as dt
import pandas as pd

# Read input Data
data_ob = dt.ob_data


# =========================================================FUNCION============================================================= #

def r_metrics_ob(data_ob: dict) -> dict:
    """
    Funcion para calcular metricas de un Orderbook

    Parameters
    ----------

    data_ob:dict (default:None)

        Datos  de entrada del Orderbook, es un diccionario con estructura siguiente:
        'timestamp': objeto tipo timestamp reconocible por maquina e.g. pd.datatime()
        'bid_size': Volumen de Bids
        'bid': Niveles de Precio del Bid
        'ask': Niveles de Precio del Ask
        'ask_size': Volumen del Asks

    Returns
    -------

    ret_data: dict

        Diccionario con las metricas calculadas:
        'No. Keys'
        'OB Time'
        'Time OB Updt'
        'Spread'
        'MidPrice'
        'Price Levels'
        'Bid Volume'
        'Ask Volume'
        'Total Volume'
        'OrdB Imb'
        'Weighted MP'
        'VW Avg Price'

    References
    ----------
    [1] https://www.geeksforgeeks.org/

    """

    # Time of Orderbook update
    ob_ts = list(data_ob.keys())
    l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]
    ob_m1 = np.median([l_ts[n_ts + 1] - l_ts[n_ts] for n_ts in range(0, len(l_ts) - 1)]).total_seconds() * 1000

    # Spread
    ob_m2 = [data_ob[ob_ts[i]]['ask'][0] - data_ob[ob_ts[i]]['bid'][0] for i in range(0, len(ob_ts))]

    # Midprice
    ob_m3 = [(data_ob[ob_ts[i]]['ask'][0] + data_ob[ob_ts[i]]['bid'][0]) * 0.5 for i in range(0, len(ob_ts))]

    # No. Price Levels
    ob_m4 = [data_ob[i_ts].shape[0] for i_ts in ob_ts]

    # Bid_Volume, Ask_Volume, Total_Volume
    ob_m5 = [np.round(data_ob[i_ts]['bid_size'].sum(), 6) for i_ts in ob_ts]
    ob_m5_1 = [np.round(data_ob[i_ts]['ask_size'].sum(), 6) for i_ts in ob_ts]
    ob_m5_2 = [np.round(data_ob[i_ts]['bid_size'].sum() + data_ob[i_ts]['ask_size'].sum(), 6) for i_ts in ob_ts]

    # Orderbook Imbalance
    # Sum(Bid Volume)/ Sum(Bid Volume , Ask Volume)
    obim = [np.round(data_ob[i]['bid_size'].sum() / (data_ob[i]['bid_size'].sum() + data_ob[i]['ask_size'].sum()), 6)
            for i in ob_ts]

    # Weighted-Midprice
    # Ask Volume/Sum(Bid Volume + Ask Volume)*Bid Price + Bid Volume/Sum(Bid Volume + Ask Volume)*Ask Price

    w_midprice = [
        (data_ob[i]['ask_size'].sum() / (data_ob[i]['bid_size'].sum() + data_ob[i]['ask_size'].sum())) * data_ob[i][
            'bid'] +
        (data_ob[i]['bid_size'].sum() / (data_ob[i]['bid_size'].sum() + data_ob[i]['ask_size'].sum())) * data_ob[i][
            'ask'] for i in ob_ts]

    # Volume-Weighted Average Price
    # Sum((Bid price * Bid Volume + Ask price * Ask volume)/ Sum(Bid Volume + Ask Volume))
    vw_midprice = [
        ((data_ob[i]['bid'].sum() * data_ob[i]['bid_size'].sum()) + (data_ob[i]['ask'] * data_ob[i]['ask_size'].sum()))
        / (data_ob[i]['bid_size'].sum() + data_ob[i]['ask_size'].sum()) for i in ob_ts]

    ret_data = {'No. Keys': ob_ts, 'OB Time': l_ts,
                'Time OB Updt': ob_m1, 'Spread': ob_m2,
                'MidPrice': ob_m3, 'Price Levels': ob_m4,
                'Bid Volume': ob_m5, 'Ask Volume': ob_m5_1,
                'Total Volume': ob_m5_2, 'OrdB Imb': obim,
                'Weighted MP': w_midprice, 'VW Avg Price': vw_midprice}

    return ret_data


def r_metrics_pt(data_pt: any) -> dict:
    n_data_pt = data_pt['side'].resample('60T').count()
    v_data_pt = data_pt['volume'].resample('60T').sum()
    t_data_pt = v_data_pt.sum()

    ret_data_pt = {'Numero de Trades': n_data_pt, 'Volumen de Trades': v_data_pt,
                   'Monto Total de Trades': t_data_pt}
    return ret_data_pt
