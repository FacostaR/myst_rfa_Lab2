
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LABORATORY 2: High-Frequency Models                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: FacostaR                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/FacostaR/myst_rfa_Lab2                                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dt
import functions as fn
import visualizations as vz
import numpy as np

# data
ob_data = dt.data
ob_ts = list(ob_data.keys())[9:]

# =======================EXPERIMENTS BY MINUTE - MIDPRICE================================== #
e1 = fn.experiments(ob_data, ob_ts, 'midprice')
#e1_plot = vz.exp1_plot(df = e1, x = 'intervalo', y = ['e1', 'e2'])
e11_mean = np.round(np.mean(e1['e1_proportion']), 2)
e12_mean = np.round(np.mean(e1['e2_proportion']), 2)

# =======================EXPERIMENTS BY MINUTE - WEIGHTED MIDPRICE========================= #
e2 = fn.experiments(ob_data, ob_ts, 'wmidprice')
#e2_plot = vz.exp1_plot(df = e2, x = 'intervalo', y = ['e1', 'e2'])
e21_mean = np.round(np.mean(e2['e1_proportion']), 2)
e22_mean = np.round(np.mean(e2['e2_proportion']), 2)

# =========================================ROLL============================================ #
# ob_ts = list(ob_data.keys())
# roll = fn.roll(ob_data, ob_ts, True)
