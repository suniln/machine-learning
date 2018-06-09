# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for yield data
file_name = 'Production_Crops_E_All_Data_(Normalized).csv'
element_code = 5419
element_name = 'yield_in_hg_per_ha'
element_unit = 'hg/ha'
# all parameter values are in hg/ha
default_selected_crops = {15 :'Wheat', 27 : 'Rice paddy',  403 : 'Onion'}

# this is our core data that we are going to predict for 3 crops
# Wheat, Rice paddy, Onion
class fao_yield_data_proc(fao_data_proc_base):
    def __init__(self, selected_crops = None):
        super(fao_yield_data_proc, self).__init__(
             default_selected_crops if selected_crops == None else selected_crops, 
             element_code, element_name, element_unit)
        
    def load_data(self):
        super().load_data(file_name)
        col_map = {'item_code_' + str(k) : 'crop' + '_' + v 
           for (k,v) in self.selected_items.items()}
        self.generate_one_hot_encoded_data(['item_code'], col_map)
