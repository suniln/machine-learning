# -*- coding: utf-8 -*-
# compiled from
# http://www.nationmaster.com/country-info/groups/High-income-OECD-countries/Agriculture
# which sources from CIA World Factbook

import pandas as pd
from utils import plots
import os

file_name = 'farm_landholding.csv'
enable_plot = True

class farm_landholding_data_proc:
    selected_country_codes = None
    countries = None
    data_folder = None
    csv_encoding = None
    def __init__(self):
        self.lh_df = None
        
    def load_data(self, file_name=file_name):
        file_path = file_name
        if farm_landholding_data_proc.data_folder:
            file_path = os.path.join(farm_landholding_data_proc.data_folder,
                        file_name)
        self.lh_df = pd.read_csv(file_path, 
                        encoding=farm_landholding_data_proc.csv_encoding)
        
    def plot(self):
        if not enable_plot:
            return
        df = self.lh_df[self.lh_df['area_code'].isin(farm_landholding_data_proc.selected_country_codes)]
        df.set_index('area_code', inplace=True)
        plots.plot_stacked_bar_chart(df, farm_landholding_data_proc.countries, 
                                     '% landholdings')
        
    # match the function signature of fao_data_proc_base
    def get_country_values(self, remove_item_code = False, one_hot_encoded=True):
        return self.lh_df
    
    # override keys - we have data only for one year
    def get_keys(self):
        return ['area_code']