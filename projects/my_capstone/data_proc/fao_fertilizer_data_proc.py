# -*- coding: utf-8 -*-
from data_proc.fao_data_proc_base import fao_data_proc_base

# parameters for fertilizer data
file_name = 'Environment_Fertilizers_E_All_Data_(Normalized).csv'
element_code = 5159
element_name = 'fert_used_kg_per_ha'
element_unit = 'kg/ha'
# all parameter values are in kg/ha
default_selected_ferts = {3102 : 'Nitrogen', 3103 : 'Phosphate',  3104 : 'Potash'}

class fao_fertilizer_data_proc(fao_data_proc_base):
    def __init__(self, selected_ferts = None):
        super(fao_fertilizer_data_proc, self).__init__(
             default_selected_ferts if selected_ferts == None else selected_ferts, 
             element_code, element_name, element_unit)
        
    def load_data(self):
        super().load_data(file_name)

    # dataset is for multiple item codes (fertilizers)
    # we need to denormalize
    # override base class definition
    def get_country_values(self, remove_item_code = True, one_hot_encoded=True):
        return super().get_country_values_denormalized(remove_item_code)