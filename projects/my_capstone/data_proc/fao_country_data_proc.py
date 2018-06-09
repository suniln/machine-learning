# -*- coding: utf-8 -*-
import pandas as pd
import os

file_name = 'country.csv'

class fao_country_data_proc:
    data_folder = None
    csv_encoding = None
    
    def __init__(self):
        self.country_df = None
        self.country_name_to_code = None
        self.country_code_to_name = None
        
    def load_data(self, file_name=file_name):
        file_path = file_name
        if fao_country_data_proc.data_folder:
            file_path = os.path.join(fao_country_data_proc.data_folder, file_name)
            
        self.country_df = pd.read_csv(file_path, 
                            encoding=fao_country_data_proc.csv_encoding)
        self.country_name_to_code = dict(zip(self.country_df['country_name'], 
                            self.country_df['area_code']))
        self.country_code_to_name = dict(zip(self.country_df['area_code'], 
                            self.country_df['country_name']))
        