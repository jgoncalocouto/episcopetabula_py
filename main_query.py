# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:00:50 2024

@author: COO1AV
"""

from tabula_extractor import *
import pandas as pd
from tabula_settings import * 
import seaborn as sns
import matplotlib.pyplot as plt

country_code = 'DE'
request_id = '1234567890123'

df_country, df_building, success = get_building_data(country_request_mask, building_request_mask, country_code, request_id)

