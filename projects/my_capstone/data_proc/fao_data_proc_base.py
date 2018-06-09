# -*- coding: utf-8 -*-

import pandas as pd
import utils.plots as plots
import os

class fao_data_proc_base:
    # static members
    countries = None # dictionary of country code/name
    selected_country_codes = None
    enable_plot = True
    data_folder = None
    csv_encoding = None
    
    '''
    parameters:
        selected_items - dictionary of item code to name
        element_code - the element we are interested in (e.g. Yield)
        element_name - this is the new column name for 'value' column
        element_unit - the unit the element is expressed in (e.g. hectogram/hectare (hg/ha))
        check_unit - perform check that all rows have the same unit as element_unit
    '''
    def __init__(self, selected_items, element_code, 
                 element_name, element_unit, check_unit = True,
                 marker = None):
        print(selected_items)
        self.selected_items = selected_items
        self.element_code = element_code
        self.element_name = element_name
        self.element_unit = element_unit
        # used for charts
        # also used for merging with other datasets if one-hot encoded fields do not
        # exist
        self.c_element_df = None
        # used for merging with other datasets if the dataset has one-hot encoded fields
        self.c_element_with_dummy_df = None 
        self.c_agg_df = None
        self.median_value_col = element_name + '_median'
        self.mean_value_col = element_name + '_mean'
        self.check_unit = check_unit
        self.marker = marker
        
    def get_keys(self):
        return ['area_code', 'year_code']
    
    def load_data(self, file_name):
        file_path = file_name
        if fao_data_proc_base.data_folder:
            file_path = os.path.join(fao_data_proc_base.data_folder, file_name)
            
        all_df = pd.read_csv(file_path, 
                    encoding=fao_data_proc_base.csv_encoding)
        # convert column names to lower case
        all_df.columns = [ x.lower().replace(' ', '_') for x in all_df.columns]
        # hack some csv files have year and year_code others have only year
        # rename year to year_code in this case
        # the two columns have same value
        if 'year_code' not in all_df.columns:
            all_df.rename(columns={'year' : 'year_code'}, inplace = True)
        # some CSV files have different column headers
        # make them all uniform
        all_df.rename(columns={'countrycode' : 'area_code', 
                               'itemcode' : 'item_code',
                               'elementcode' : 'element_code'
                               }, inplace = True)
        
        # check that element is expressed in same units for all records
        # should check on unit for 'hg/ha' should return True for all()
        # hectogram / hectare
        # hectogram = 100 grams
        if self.check_unit and not (all_df[all_df['element_code'] == self.element_code]['unit'] == self.element_unit).all():
            raise Exception(self.element_name + ' not in same units. Expected:' + 
                            self.element_unit +
                            ", Found:" + str(all_df[all_df['element_code'] == self.element_code]['unit'].unique()))
    
        # Select only items that we want. e.g. wheat, rice, Onions
        # select only country code, year and yield
        selected_df = all_df[
                    (all_df['item_code'].isin(self.selected_items.keys())) & 
                    (all_df['element_code'] == self.element_code)
                ].loc[:, ['item_code', 'area_code', 'year_code', 'value']]
        selected_df.rename(columns={'value' : self.element_name}, inplace = True)
        
        print('selected_df', selected_df)
        # element for countries (this is time series of year)
        self.c_element_df = selected_df[selected_df['area_code'].isin(fao_data_proc_base.countries.keys())]
        print('c_element_df', self.c_element_df)
        
        # select only 4 recent years (our data is ordered in assending order of year)
        # for aggregation
        c_element_latest = self.c_element_df.groupby(['item_code', 'area_code']).tail(4)
        print('c_element_latest', c_element_latest)
        c_element_grouped = c_element_latest.groupby(['item_code', 'area_code'], as_index=False)
        print('c_element_grouped', c_element_grouped)
        # get aggregate element value for each of the items by country
        self.c_agg_df = c_element_grouped[self.element_name].agg(['median', 'min', 'mean', 'max', 'std'])
        print('c_agg_df', self.c_agg_df)
        self.c_agg_df.columns = [self.element_name + '_' + col for col in self.c_agg_df.columns]

    def generate_one_hot_encoded_data(self, column_names, column_map):
        self.c_element_with_dummy_df = pd.get_dummies(
                self.c_element_df, columns=column_names)
        self.c_element_with_dummy_df.rename(columns=column_map, 
                                            inplace = True)
    
    def get_country_values(self, remove_item_code = False, one_hot_encoded = True):
        # if dataset has data only for one year then exclude year_code
        # the keys in this case would be only area_code
        df = self.c_element_df if self.c_element_with_dummy_df is None else self.c_element_with_dummy_df
        if not one_hot_encoded:
            df = self.c_element_df
        columns = df.columns
        exclude_columns = self.get_columns_to_exclude()
        if remove_item_code:
            exclude_columns.add('item_code')
        return df[columns[~columns.isin(exclude_columns)]]
    
    def get_country_values_denormalized(self, remove_item_code = True):
        dfs = []
        exclude_columns = self.get_columns_to_exclude()
        # we remove item_code column in denormalized datasets by default
        if remove_item_code:
            exclude_columns.add('item_code') 
        for item_code in self.selected_items.keys():
            df = self.c_element_df if self.c_element_with_dummy_df is None else self.c_element_with_dummy_df
            df = df[df['item_code'] == item_code]
            #df = df.drop(['item_code'], axis=1)
            df = df[df.columns[~df.columns.isin(exclude_columns)]]
            df.rename(columns={self.element_name : self.element_name + '_' + self.selected_items[item_code]}, inplace=True)
            dfs.append(df)
        df = None
        if len(dfs) > 0:
            df = dfs[0]
        if len(dfs) > 1:
            for d in dfs[1:]:
                df = pd.merge(df, d, on=self.get_keys(), how='outer')
        return df
    
    # some data sets do not have year_code as key
    # remove year_code from such datasets
    def get_columns_to_exclude(self):
        return {'year_code'}.difference(self.get_keys())
    
    def get_country_agg_values(self):
        return self.c_agg_df[self.mean_value_col]

    def plot_all(self, selected_country_codes = None):
        if not fao_data_proc_base.enable_plot:
            return
        self.plot_agg_values_for_all_countries()
        self.plot_values_for_selected_countries_over_time(selected_country_codes)
        
    def plot_agg_values_for_all_countries(self):
        # plot aggregate yields for selected crops and all countries
        for item_code in self.selected_items.keys():
            plots.plot_agg_element(self.c_agg_df, item_code,
                fao_data_proc_base.countries,
                self.median_value_col, self.mean_value_col,
                'country', self.element_unit,
                self.selected_items[item_code], self.element_name)
    
    def plot_values_for_selected_countries_over_time(self, selected_country_codes = None):
        for item_code in self.selected_items.keys():
            plots.plot_element_for_item_over_time(self.c_element_df, 
                fao_data_proc_base.selected_country_codes if selected_country_codes == None else selected_country_codes, 
                fao_data_proc_base.countries, item_code, 
                self.element_name,
                self.selected_items[item_code] + ' ' + self.element_name + ' ' + self.element_unit,
                self.marker)

    def get_stats(self):
        self.c_element_df.groupby('area_code')['year_code'].unique().count()