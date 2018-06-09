# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# energy used in aggriculture as % of total energy used
file_name = 'Environment_Energy_E_All_Data.csv'
element_code = 72040
element_name = 'perc_of_total_energy_used_for_agri'
element_unit = '%'
# all parameter values are in US$
default_selected_parameters = {6741 : 'Energy Used In Agg'}

class fao_energy_used_data_proc(fao_data_proc_base):
    def __init__(self, selected_parameters = None):
        super(fao_energy_used_data_proc, self).__init__(
             default_selected_parameters if selected_parameters == None else selected_parameters, 
             element_code, element_name, element_unit, False) # do not check unit since it is NAN in the df
        
    def load_data(self):
        super().load_data(file_name)
    