# -*- coding: utf-8 -*-
# compiled from
# http://www.nationmaster.com/country-info/groups/High-income-OECD-countries/Agriculture
# which sources from CIA World Factbook

import pandas as pd
import os

file_name = 'country_region.csv'

class country_region_data_proc:
    data_folder = None
    csv_encoding = None
    r_code_to_name = None
    i_code_to_name = None
    
    def __init__(self):
        self.c_r_df = None
        self.c_r_with_dummy_df = None
        self.c_r_code_to_data = dict()
        
    def load_data(self, file_name = file_name):
        file_path = file_name
        if country_region_data_proc.data_folder:
            file_path = os.path.join(country_region_data_proc.data_folder,
                            file_name)
        self.c_r_df = pd.read_csv(file_path, 
                            encoding=country_region_data_proc.csv_encoding)
        self.c_r_df = self.c_r_df.drop(['region', 'income', 'country_name', 'landholdings'], 
                                       axis=1)
        print(self.c_r_df)
        # one-hot encode region_code
        col_map = {'region_code_' + str(k) : 'region' + '_' + v 
           for (k,v) in country_region_data_proc.r_code_to_name.items()}
        
        self.generate_one_hot_encoded_data(self.c_r_df, 
                                    ['region_code'], col_map)
        # one-hot encode income_code
        col_map = {'income_code_' + str(k) : 'income' + '_' + v 
           for (k,v) in country_region_data_proc.i_code_to_name.items()}
        
        self.generate_one_hot_encoded_data(self.c_r_with_dummy_df, 
                                    ['income_code'], col_map)
        
        for index, row in self.c_r_df.iterrows():
            self.c_r_code_to_data[row['area_code']] = \
                            {
                             'region_code' : row['region_code'],
                             'income_code' : row['income_code']
                            }
    
    def get_keys(self):
        return ['area_code']
    
    # keep same signature as fao_data_proc_base
    def get_country_values(self, remove_item_code = False, one_hot_encoded=True):
        df = self.c_r_df
        if one_hot_encoded:
            df = self.c_r_with_dummy_df
        return df
    
    def generate_one_hot_encoded_data(self, df, column_names, column_map):
        self.c_r_with_dummy_df = pd.get_dummies(
                df, columns=column_names)
        self.c_r_with_dummy_df.rename(columns=column_map, 
                                            inplace = True)
