import pandas as pd
import os

file_name = 'region.csv'

class region_data_proc:
    data_folder = None
    csv_encoding = None
    def __init__(self):
        self.r_df = None
        self.r_name_to_code = dict()
        self.r_code_to_name = dict()
        
    def load_data(self, file_name = file_name):
        file_path = file_name
        if region_data_proc.data_folder:
            file_path = os.path.join(region_data_proc.data_folder,
                            file_name)
        self.r_df = pd.read_csv(file_path, 
                            encoding=region_data_proc.csv_encoding)
        self.r_name_to_code = dict(zip(self.r_df['region_name'], 
                            self.r_df['region_code']))
        self.r_code_to_name = dict(zip(self.r_df['region_code'], 
                            self.r_df['region_name']))
