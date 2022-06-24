
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LABORATORY 2: High-Frequency Models                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: FacostaR                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/FacostaR/myst_rfa_Lab2                                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from pandas import DataFrame
import plotly.express as px
import numpy as np

import data as dt
import functions as fn
import pandas as pd

def exp1_plot(df: DataFrame, x: str, y: str) -> 'stackedbarplot':
    """
    Function used to plot a stacked bar for experiment 1

    arguments:
    ----------
    df: DataFrame
    DataFrame containing results from a martingale analysis

    x: str
    x-axis (0-59 minutes)

    y: str
    y-axis (martingales and non martingales)

    Returns -> stacked barplot 
    """
    fig = px.bar(df, x=x, y=y, title='martingale experiment', labels=dict(x=np.arange(0,59)))
    fig.update_layout(
        xaxis = {'type' : 'category'},
        xaxis_title_text='Interval', # xaxis label
        yaxis_title_text='occurrences' # yaxis label
        )
    return fig.show()





def plot_roll(x,y,option, show = False):
    ''' 
    Function created with the purpose of plotting the created variables

     arguments:
    ----------
    x: List
    List containing timestamps of str type

    y: DataFrame
    DataFrame containing results from a roll model analysis
    
    '''
    
    ob_data = x
    ob_ts = list(ob_data.keys())
    y['prices'] = [(ob_data[ob_ts[i]]['ask'][0] + ob_data[ob_ts[i]]['bid'][0])*.5 for i in range(0, len(ob_ts))]
    y['x'] = ob_ts

    if option == 'theorical':
        fig = px.line(y, x = 'x', y = ['theorical_ask','theorical_bid','prices'], title = 'Theorical values')
    

    elif option == 'observed':
        fig = px.line(y, x = 'x', y = ['observed_ask','observed_bid','prices'], title = 'Observed values')
    
    if show:
        fig.show()
    


final_roll_model = fn.roll_model(dt.data)
df_roll = pd.DataFrame({'observed_ask':final_roll_model['observed_ask'],'observed_bid':final_roll_model['observed_bid'],'theorical_ask':final_roll_model['theorical_ask'],'theorical_bid':final_roll_model['theorical_bid']})

