# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# compiled from
# http://www.nationmaster.com/country-info/groups/High-income-OECD-countries/Agriculture
# which sources from CIA World Factbook
# reformatted to be compliant with FAO datasets
file_name = 'tractors_used.csv'
element_code = 2
element_name = 'tractors_per_100_ha'
element_unit = 'count'
# all parameter values are in US$
default_selected_parameters = {101 : 'tractors'}

class tractors_used_data_proc(fao_data_proc_base):
    def __init__(self, selected_parameters = None):
        super(tractors_used_data_proc, self).__init__(
             default_selected_parameters if selected_parameters == None else selected_parameters, 
             element_code, element_name, element_unit, False,
             marker = 'o') # we have this data only for one year... use marker
        
    def load_data(self):
        super().load_data(file_name)

    # we have data for 2003 only
    def get_keys(self):
        return ['area_code']