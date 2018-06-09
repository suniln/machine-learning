# -*- coding: utf-8 -*-
import pandas as pd
import os

file_name = 'region.csv'

class fao_region_data_proc:
    data_folder = None
    csv_encoding = None
    
    def __init__(self):
        self.region_df = None
        self.region_name_to_code = None
        self.region_code_to_name = None
        
    def load_data(self, file_name=file_name):
        file_path = file_name
        if fao_region_data_proc.data_folder:
            file_path = os.path.join(fao_region_data_proc.data_folder, file_name)
            
        self.region_df = pd.read_csv(file_path, 
                            encoding=fao_region_data_proc.csv_encoding)
        self.region_name_to_code = dict(zip(self.region_df['region_name'], 
                            self.region_df['region_code']))
        self.region_code_to_name = dict(zip(self.region_df['region_code'], 
                            self.region_df['region_name']))
        