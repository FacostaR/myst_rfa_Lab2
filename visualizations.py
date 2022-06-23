
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

def exp1_plot(df: DataFrame, x: str, y: str) -> 'stackedbarplot':
    """
    Function used to plot a stacked bar plot

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
    fig = px.bar(df, x=x, y=y, title='martingale experiment')
    fig.show()








