# -*- coding: utf-8 -*-

import pandas as pd
import os

file_name = 'income.csv'

class income_data_proc:
    data_folder = None
    csv_encoding = None
    def __init__(self):
        self.i_df = None
        self.i_name_to_code = dict()
        self.i_code_to_name = dict()
        
    def load_data(self, file_name = file_name):
        file_path = file_name
        if income_data_proc.data_folder:
            file_path = os.path.join(income_data_proc.data_folder,
                            file_name)
        self.i_df = pd.read_csv(file_path, 
                            encoding=income_data_proc.csv_encoding)
        self.i_name_to_code = dict(zip(self.i_df['income_name'], 
                            self.i_df['income_code']))
        self.i_code_to_name = dict(zip(self.i_df['income_code'], 
                            self.i_df['income_name']))
