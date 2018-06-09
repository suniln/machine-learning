# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for water use data
file_name = 'Environment_Water_E_All_Data.csv'
element_code = 7222
element_name = 'water_used_in_agri_as_perc_of_total_water_used'
element_unit = '%'
# all parameter values are in percentage of total water withdrawal
default_water_use_parameters = {6720 : 'water used for agg'}

class fao_water_use_data_proc(fao_data_proc_base):
    def __init__(self, selected_parameters = None):
        super(fao_water_use_data_proc, self).__init__(
             default_water_use_parameters if selected_parameters == None else selected_parameters, 
             element_code, element_name, element_unit)
        
    def load_data(self):
        super().load_data(file_name)
