# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# amongst macro statistics we will use gdp per capita in USD
file_name = 'Macro-Statistics_Key_Indicators_E_All_Data_(Normalized).csv'
element_code = 6119
element_name = 'gdp_per_capita_usd'
element_unit = 'USD'
# all parameter values are in US$
default_selected_parameters = {22014 : 'GDP Per Capita USD'}

class fao_economic_data_proc(fao_data_proc_base):
    def __init__(self, selected_parameters = None):
        super(fao_economic_data_proc, self).__init__(
             default_selected_parameters if selected_parameters == None else selected_parameters, 
             element_code, element_name, element_unit, False) # do not check unit since it is NAN in the df
        
    def load_data(self):
        super().load_data(file_name)

