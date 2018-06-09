# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for soil data
file_name = 'Environment_Soil_E_All_Data.csv'
element_code = 7219
element_name = 'soil_erosion_average_in_GLASOD_degrees'
element_unit = 'degrees'
# all parameters values are in kg/ha
default_soil_erosion_parameters = {6709 :'Soil Erosion'}

class fao_soil_erosion_data_proc(fao_data_proc_base):
    def __init__(self, soil_erosion_parameters = None):
        super(fao_soil_erosion_data_proc, self).__init__(
             default_soil_erosion_parameters if soil_erosion_parameters == None else soil_erosion_parameters, 
             element_code, element_name, element_unit, 
             marker = 'o') # since we have data only for one year we will print marker on line graph
        
    def load_data(self):
        super().load_data(file_name)
        
    # we have data only for 1991
    def get_keys(self):
        return ['area_code']