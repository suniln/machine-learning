# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for land use data
file_name = 'Environment_LandUse_E_All_Data_(Normalized).csv'
element_code = 7208
element_name = 'percent_agg_land'
element_unit = '%'
# all parameter values are in percentage of aggricultural land
default_land_use_parameters = {6621 :'arable_land', 
                          6650 : 'permanent_crops',  
                          6655 : 'permanent_meadows',
                          6611 : 'irrigated',
                          6690 : 'equiped_for_irrigation'}

class fao_land_use_data_proc(fao_data_proc_base):
    def __init__(self, land_use_parameters = None):
        super(fao_land_use_data_proc, self).__init__(
             default_land_use_parameters if land_use_parameters == None else land_use_parameters, 
             element_code, element_name, element_unit)
        
    def load_data(self):
        super().load_data(file_name)
    
    # dataset is for multiple item codes (fertilizers)
    # we need to denormalize
    # override base class definition
    def get_country_values(self, remove_item_code = True, one_hot_encoded=True):
        return super().get_country_values_denormalized()