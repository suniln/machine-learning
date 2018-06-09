# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for pesticide data
file_name = 'Environment_Pesticides_E_All_Data_(Normalized).csv'
element_code = 5159
element_name = 'pesticide_average_use_in_kg_per_ha'
element_unit = 'kg/ha'
# all parameters values are in kg/ha
default_pesticide_parameters = {1357 :'pesticides'}

class fao_pesticide_data_proc(fao_data_proc_base):
    def __init__(self, pesticide_parameters = None):
        super(fao_pesticide_data_proc, self).__init__(
             default_pesticide_parameters if pesticide_parameters == None else pesticide_parameters, 
             element_code, element_name, element_unit)
        
    def load_data(self):
        super().load_data(file_name)
    