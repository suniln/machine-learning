# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for soil data
file_name = 'Environment_Soil_E_All_Data.csv'
element_code = 7221
element_name = 'carbon_in_topsoil_average_perc_in_weight'
element_unit = '%'
# all parameters values are in %
default_soil_carbon_content_parameters = {6709 :'Topsoil Carbon Content'}

class fao_soil_carbon_content_data_proc(fao_data_proc_base):
    def __init__(self, soil_carbon_content_parameters = None):
        super(fao_soil_carbon_content_data_proc, self).__init__(
             default_soil_carbon_content_parameters if soil_carbon_content_parameters == None else soil_carbon_content_parameters, 
             element_code, element_name, element_unit, 
             marker = 'o') # since we have data only for one year we will print marker on line graph
        
    def load_data(self):
        super().load_data(file_name)
        
