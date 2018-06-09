    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:21:27 2017

@author: sunil

Here we load all the agriculture data for all countries and years available
and denormalize values for items into separate columns
e.g.: data for fertilizers N,P,K are normalized, we create one columns for each
      fertilizer
"""

import app_settings
import pandas as pd

output_file_name = app_settings.combined_output_file_name
output_file_name_encoded = app_settings.combined_output_file_name_encoded

enable_charts = True

cols = ['area_code', 'year_code', 'yield_in_hg_per_ha', 'crop_wheat',
       'crop_rice_paddy', 'crop_onion', 'region_East Asia and the Pacific',
       'region_Europe and Central Asia', 'region_High-income',
       'region_Latin America and the Caribbean',
       'region_Middle East and North Africa', 'region_South Asia',
       'region_Sub-Saharan Africa', 'income_Low-income',
       'income_Lower-middle-income', 'income_Upper-middle-income',
       'income_High-income', 'fert_used_kg_per_ha_Nitrogen',
       'fert_used_kg_per_ha_Phosphate', 'fert_used_kg_per_ha_Potash',
       'percent_agg_land_arable_land', 'percent_agg_land_permanent_crops',
       'percent_agg_land_permanent_meadows', 'percent_agg_land_irrigated',
       'percent_agg_land_equiped_for_irrigation',
       'pesticide_average_use_in_kg_per_ha',
       'water_used_in_agri_as_perc_of_total_water_used', 'gdp_per_capita_usd',
       'perc_of_total_energy_used_for_agri',
       'soil_erosion_average_in_GLASOD_degrees',
       'soil_degradation_average_in_GLASOD_degrees',
       'carbon_in_topsoil_average_perc_in_weight', 'country_name', 'lt_1_ha',
       '1_2_ha', '2_5_ha', '5_10_ha', '10_20_ha', '20_50_ha', '50_100_ha',
       '100_200_ha', '200_500_ha', '500_1000_ha', 'gt_1000_ha',
       'workers_per_ha', 'tractors_per_100_ha']
short_cols = ['area_code', 'year_code', 'yield', 'Wheat',
       'Rice', 'Onion', 'R_EA_P',
       'R_E_CA', 'R_HI',
       'R_LAm_C',
       'R_ME_NAf', 'R_SA',
       'R_SSAf', 'I_LI',
       'I_LMI', 'I_UMI',
       'I_HI', 'F_N',
       'F_P', 'F_K',
       'L_AL', 'L_PC',
       'L_PM', 'L_I',
       'L_EI',
       'Pest',
       'W', 'GDP',
       'Enrg',
       'S_Ero',
       'S_Deg',
       'C', 'country_name',
       'lt_1h', # Region Avg if na
       '1_2h', # Region Avg if na
       '2_5h', # Region Avg if na
       '5_10h', # Region Avg if na
       '10_20h', # Region Avg if na
       '20_50h', # Region Avg if na
       '50_1hh', # Region Avg if na
       '1h_2hh', # Region Avg if na
       '2h_5hh', # Region Avg if na
       '5h_1kh', # Region Avg if na
       'gt_1kh', # Region Avg if na
       'Wkr', 
       'Trk']

# Data extraction from:
# # http://www.nationmaster.com/country-info/groups/High-income-OECD-countries/Agriculture
from data_proc.region_data_proc import region_data_proc
from data_proc.income_data_proc import income_data_proc
from data_proc.country_region_data_proc import country_region_data_proc
from data_proc.farm_landholding_data_proc import farm_landholding_data_proc
# FAO data
# http://www.fao.org/faostat/en/#home
# data bulk downloaded and saved to data folder
from data_proc.fao_country_data_proc import fao_country_data_proc
from data_proc.fao_data_proc_base import fao_data_proc_base
from data_proc.fao_yield_data_proc import fao_yield_data_proc
from data_proc.fao_fertilizer_data_proc import fao_fertilizer_data_proc
from data_proc.fao_land_use_data_proc import fao_land_use_data_proc
from data_proc.fao_pesticide_data_proc import fao_pesticide_data_proc
from data_proc.fao_water_use_data_proc import fao_water_use_data_proc
from data_proc.fao_economic_data_proc import fao_economic_data_proc
from data_proc.fao_energy_used_data_proc import fao_energy_used_data_proc
from data_proc.fao_soil_erosion_data_proc import fao_soil_erosion_data_proc
from data_proc.fao_soil_degradation_data_proc import fao_soil_degradation_data_proc
from data_proc.fao_soil_carbon_content_data_proc import fao_soil_carbon_content_data_proc
from data_proc.farm_workers_data_proc import farm_workers_data_proc
from data_proc.tractors_used_data_proc import tractors_used_data_proc

#import os
#dir_path = os.path.join(os.getcwd(), 'project')
#print(dir_path)
#os.chdir(dir_path)

# the aim of this project is to determine the factors impacting the yield of
# agricultural land for various crop types

# there is no precanned available data in the form required for this project
# we will have to consolidate data from different sources

# For this project I intend to work with 3 kinds of crops: 
# wheat, rice paddy and onion
# we limit our analysis to these crops
# values in hectogram/hectare
selected_crops = {15 :'wheat', 
                  27 : 'rice_paddy',  
                  403 : 'onion'}
# these are generic fertilizer for which we have data
# values in kilograms/hectare
selected_ferts = {3102 : 'Nitrogen', 
                  3103 : 'Phosphate',  
                  3104 : 'Potash'}
# land use attributes. 
# values percentage of aggrugultural land.
selected_land_use_parameters = {6621 :'arable_land', 
                  6650 : 'permanent_crops',  
                  6655 : 'permanent_meadows',
                  6611 : 'irrigated',
                  6690 : 'equiped_for_irrigation'}

# pesticide attributes
# values are in kilograms/hectare
selected_pesticide_parameters = {1357 :'pesticides'}
# water use parameters
selected_water_use_parameters = {6720 : 'water used for agg'}
# macro economic parameters
selected_economic_parameters = {22014 : 'GDP Per Capita'}
# energy used in aggriculture
selected_energy_parameters = {6741 : 'Energy Used In Agg'}
# soil erosion parameters
selected_soil_erosion_parameters = {6709 :'Soil Erosion'}
# soil degradation parameters
selected_soil_degradation_parameters = {6709 :'Soil Degradation'}
# topsoil carbon content % weight
selected_soil_carbon_content_parameters = {6709 :'Topsoil Carbon Content'}
# some countries of interest for plotting only:
# Australia 10 - Region: Australia and New Zealand
# Brazil 21 - Region: South America
# China 41 - Region: Asia
# India 100 - Region: South Asia
# Japan 110 - Region: East Asia
# Mexico 138 - Region: Central America
# Nigeria 159 - Africa
# South Africa 202 - Region Africa
# USA 231 - Region: North America
selected_country_codes = [10, 21, 41, 100, 110, 138, 159, 202, 231]
selected_countries = None

# NON FAO DATA
# Data compiled from NationMaster which sources from CIA World Factbook 
# http://www.nationmaster.com/country-info/stats/Agriculture
selected_workers_parameters = {100 : 'Workers'}
selected_tractors_parameters = {101 : 'Tractors'}
# LANDHOLDING data has been curated by hand from NationMaster report

# country data
country_df = None
c_name_to_code = None
c_code_to_name = None

# region
region_df = None
r_name_to_code = None
r_code_to_name = None

# income
income_df = None
i_name_to_code = None
i_code_to_name = None

# country region
country_region_df = None
c_r_code_to_data = None

# data proc instances
country_data_proc = fao_country_data_proc()
r_data_proc = region_data_proc()
i_data_proc = income_data_proc()
c_r_data_proc = country_region_data_proc()

yield_data_proc = fao_yield_data_proc(selected_crops)
fertilizer_data_proc = fao_fertilizer_data_proc(selected_ferts)
land_use_data_proc = fao_land_use_data_proc(selected_land_use_parameters)
water_use_data_proc = fao_water_use_data_proc(selected_water_use_parameters)
pesticide_data_proc = fao_pesticide_data_proc(selected_pesticide_parameters)
economic_data_proc = fao_economic_data_proc(selected_economic_parameters)
energy_used_data_proc = fao_energy_used_data_proc(selected_energy_parameters)
soil_erosion_data_proc = fao_soil_erosion_data_proc(selected_soil_erosion_parameters)
soil_degradation_data_proc = fao_soil_degradation_data_proc(selected_soil_degradation_parameters)
soil_carbon_content_data_proc = fao_soil_carbon_content_data_proc(selected_soil_carbon_content_parameters)
pesticide_data_proc = fao_pesticide_data_proc(selected_pesticide_parameters)
landholding_data_proc = farm_landholding_data_proc()
workers_data_proc = farm_workers_data_proc(selected_workers_parameters)
tractors_data_proc = tractors_used_data_proc(selected_tractors_parameters)

# load countries
def load_countries():
    global country_df
    global c_name_to_code
    global c_code_to_name
    global selected_countries
    fao_country_data_proc.data_folder = app_settings.data_folder
    fao_country_data_proc.csv_encoding = app_settings.csv_encoding
    country_data_proc.load_data()
    country_df = country_data_proc.country_df
    c_name_to_code = country_data_proc.country_name_to_code
    c_code_to_name = country_data_proc.country_code_to_name
    selected_countries = { x: c_code_to_name[x] for x in [10, 21, 41, 100, 110, 138, 159, 202, 231]}

def load_regions():
    global region_df
    global r_name_to_code
    global r_code_to_name
    region_data_proc.data_folder = app_settings.data_folder
    region_data_proc.csv_encoding = app_settings.csv_encoding
    r_data_proc.load_data()
    region_df = r_data_proc.r_df
    r_name_to_code = r_data_proc.r_name_to_code
    r_code_to_name = r_data_proc.r_code_to_name

def load_income():
    global income_df
    global i_name_to_code
    global i_code_to_name
    income_data_proc.data_folder = app_settings.data_folder
    income_data_proc.csv_encoding = app_settings.csv_encoding
    i_data_proc.load_data()
    income_df = i_data_proc.i_df
    i_name_to_code = i_data_proc.i_name_to_code
    i_code_to_name = i_data_proc.i_code_to_name

# country regions
def load_country_region():
    global country_region_df
    global c_r_name_to_data
    global c_r_code_to_data
    country_region_data_proc.data_folder = app_settings.data_folder
    country_region_data_proc.csv_encoding = app_settings.csv_encoding
    country_region_data_proc.r_code_to_name = r_code_to_name
    country_region_data_proc.i_code_to_name = i_code_to_name
    c_r_data_proc.load_data()
    country_region_df = c_r_data_proc.c_r_df
    c_r_code_to_data = c_r_data_proc.c_r_code_to_data

# load yield data
def load_yield_data():
    yield_data_proc.load_data()
    yield_data_proc.plot_all()

# load fertilizer data
def load_fertilizer_data():
    fertilizer_data_proc.load_data()
    fertilizer_data_proc.plot_all()

# load land use data
def load_land_use_data():
    land_use_data_proc.load_data()
    land_use_data_proc.plot_all()

# pesticide data
def load_pesticide_data():
    pesticide_data_proc.load_data()
    pesticide_data_proc.plot_all()

# water use data
def load_water_use_data():
    water_use_data_proc.load_data()
    water_use_data_proc.plot_all()

# macro economic parameters
def load_economic_data():
    economic_data_proc.load_data()
    economic_data_proc.plot_all()

# energy used
def load_energy_used_data():
    energy_used_data_proc.load_data()
    energy_used_data_proc.plot_all()

# soil erosion
def load_soil_erosion_data():
    soil_erosion_data_proc.load_data()
    soil_erosion_data_proc.plot_all()

# soil degradation
def load_soil_degradation_data():
    soil_degradation_data_proc.load_data()
    soil_degradation_data_proc.plot_all()

# topsoil carbon content
def load_carbon_content_data():
    soil_carbon_content_data_proc.load_data()
    soil_carbon_content_data_proc.plot_all()

# land holding data (farm size)
def load_landholding_data():
    landholding_data_proc.load_data()
    landholding_data_proc.plot()

# farm workers data
def load_farm_workers_data():
    workers_data_proc.load_data()
    workers_data_proc.plot_all()

# tractors data
def load_tractors_data():
    tractors_data_proc.load_data()
    tractors_data_proc.plot_all()

def merge_df(first, second, how='left', one_hot_encoded = False):
    return first.merge(
        second.get_country_values(remove_item_code = True, 
                                  one_hot_encoded = one_hot_encoded), 
        on=second.get_keys(), how=how)

# data generation
# Most of the data is gathered from: 
# Food And Agriculture Organization 
# load country and region data from Food And Agruculture Organization
# United Nations (http://www.fao.org/faostat/en/#data)
def load_basic_data(plot_charts = False):
    load_countries()
    load_regions()
    load_income()
    load_country_region()
    # set static members
    fao_data_proc_base.countries = c_code_to_name
    fao_data_proc_base.selected_country_codes = selected_country_codes
    fao_data_proc_base.data_folder = app_settings.data_folder
    fao_data_proc_base.csv_encoding = app_settings.csv_encoding
    # if set this to true for plot_all() returns without plotting the data
    fao_data_proc_base.enable_plot = plot_charts
    #landholding data from NationMaster.com
    farm_landholding_data_proc.selected_country_codes = selected_country_codes
    farm_landholding_data_proc.countries = c_code_to_name
    farm_landholding_data_proc.data_folder = app_settings.data_folder
    farm_landholding_data_proc.csv_encoding = app_settings.csv_encoding
    farm_landholding_data_proc.enable_plot = plot_charts
    
# load Food And Agriculture Organization data
def load_agri_data():
    # we restrict this to all countries for which regions are defined
    # also exclude Sudan (has now split in 2 countries so historical data is ambiguous)
    load_yield_data()
    load_fertilizer_data()
    load_land_use_data()
    load_pesticide_data()
    load_water_use_data()
    load_economic_data()
    load_energy_used_data()
    load_soil_erosion_data()
    load_soil_degradation_data()
    load_carbon_content_data()
    load_landholding_data()
    load_farm_workers_data()
    load_tractors_data()
    
# merge all the data to create a data frame with all columns
def merge_data(one_hot_encoded = True):
    # start with yield data for Wheat, Rice paddy and Onions
    # this will be our main dataset
    # all other datasets will join using yield and left outer dataset
    df_all = yield_data_proc.get_country_values(one_hot_encoded = one_hot_encoded)
    print("yield data", df_all.shape)
    # merge country and region information with yield data (inner join)
    # this will eliminate countries for which we do not have good data
    # e.g. Sudan (country split and historic data is confusing) and few
    # smaller islands that are autonomous regions of bigger countries
    # e.g. Guam
    df_all = merge_df(df_all, c_r_data_proc, how='inner', one_hot_encoded = one_hot_encoded)
    print("yield data with region and income", df_all.shape)    
    # merge with fertilizer data
    df_all = merge_df(df_all, fertilizer_data_proc, one_hot_encoded = one_hot_encoded)
    print("added fertilizer data", df_all.shape)
    # merge with land use data
    df_all = merge_df(df_all, land_use_data_proc, one_hot_encoded = one_hot_encoded)
    print("added land use data", df_all.shape)
    # merge pesticide data
    df_all = merge_df(df_all, pesticide_data_proc, one_hot_encoded = one_hot_encoded)
    print("added pesticide data", df_all.shape)
    # merge water use data
    df_all = merge_df(df_all, water_use_data_proc, one_hot_encoded = one_hot_encoded)
    print("added water use data", df_all.shape)
    # merge with economic data
    df_all = merge_df(df_all, economic_data_proc, one_hot_encoded = one_hot_encoded)
    print("added economic data", df_all.shape)
    # merge energy used data
    df_all = merge_df(df_all, energy_used_data_proc, one_hot_encoded = one_hot_encoded)
    print("added energy used data", df_all.shape)
    # merge soil erosion data 
    df_all = merge_df(df_all, soil_erosion_data_proc, one_hot_encoded = one_hot_encoded)
    print("added soil erosion data", df_all.shape)
    # merge soil degradation data
    df_all = merge_df(df_all, soil_degradation_data_proc, one_hot_encoded = one_hot_encoded)
    print("added soil degradation data", df_all.shape)
    # merge soil carbon content data
    df_all = merge_df(df_all, soil_carbon_content_data_proc, one_hot_encoded = one_hot_encoded)
    print("added carbon content data", df_all.shape)
    # merge landholding data
    df_all = merge_df(df_all, landholding_data_proc, one_hot_encoded = one_hot_encoded)
    print("added landholding data", df_all.shape)
    # merge farm workers data
    df_all = merge_df(df_all, workers_data_proc, one_hot_encoded = one_hot_encoded)
    print("added workers data", df_all.shape)
    # merge tractors data
    df_all = merge_df(df_all, tractors_data_proc, one_hot_encoded = one_hot_encoded)
    print("added tractors data", df_all.shape)
    rename_columns(df_all)
    file_name = output_file_name
    # write merged data to csv
    if one_hot_encoded:
        file_name = output_file_name_encoded
    df_all.to_csv(app_settings.get_data_file(file_name), index=False)

def read_merged_agri_data(one_hot_encoded=True):
    file_name = output_file_name
    # write merged data to csv
    if one_hot_encoded:
        file_name = output_file_name_encoded
    return pd.read_csv(app_settings.get_data_file(file_name),
                encoding=app_settings.csv_encoding)

# we load and merge all data and create two files.
# one with categorical data encoded
# and one without encoding categorical data (convenient to use for plots)
def load_and_merge_all_data():
    load_basic_data(enable_charts)
    load_agri_data()
    merge_data(one_hot_encoded=False)
    merge_data()
    
def rename_columns(df):
    # rename columns so the graphs are not too cluttered
    cols_to_short_name = dict(zip(cols, short_cols))
    #cols_from_short_name = dict(zip(short_cols, cols))
    df.rename(columns=cols_to_short_name, inplace=True)

if __name__ == '__main__':
    load_and_merge_all_data()
