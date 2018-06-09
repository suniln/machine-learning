# -*- coding: utf-8 -*-
from pandas import DataFrame
from sklearn.model_selection import train_test_split
import app_settings

def generate_files():
    all_df = DataFrame.from_csv(app_settings.get_data_file(app_settings.final_agri_file_name))
    all_df['gt_1hh'] = all_df['1h_2hh'] + all_df['2h_5hh'] + \
        all_df['5h_1kh'] + all_df['gt_1kh']
    wheat_df = all_df[all_df['item_code'] == 15]
    rice_df = all_df[all_df['item_code'] == 27]
    onion_df = all_df[all_df['item_code'] == 403]
    
    # create datasets for wheat and save
    wheat_train, wheat_test = train_test_split(wheat_df, test_size=0.2, shuffle=True)
    wheat_train.to_csv(app_settings.get_data_file('wheat' + app_settings.train_file_name_suffix))
    wheat_test.to_csv(app_settings.get_data_file('wheat' + app_settings.test_file_name_suffix))
    
    # create datasets for rice and save
    rice_train, rice_test = train_test_split(rice_df, test_size=0.2, shuffle=True)
    rice_train.to_csv(app_settings.get_data_file('rice' + app_settings.train_file_name_suffix))
    rice_test.to_csv(app_settings.get_data_file('rice' + app_settings.test_file_name_suffix))
    
    # create datasets for onion and save
    onion_train, onion_test = train_test_split(onion_df, test_size=0.2, shuffle=True)
    onion_train.to_csv(app_settings.get_data_file('onion' + app_settings.train_file_name_suffix))
    onion_test.to_csv(app_settings.get_data_file('onion' + app_settings.test_file_name_suffix))

def get_train_test_data(item_name):
    train_df = DataFrame.from_csv(
            app_settings.get_data_file(item_name + app_settings.train_file_name_suffix)
        )
    test_df = DataFrame.from_csv(
            app_settings.get_data_file(item_name + app_settings.test_file_name_suffix)
        )
    return (train_df, test_df)