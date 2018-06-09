# -*- coding: utf-8 -*-
from pandas import DataFrame
import app_settings
import prepare_data
from utils import plots

input_file = app_settings.final_agri_file_name
# dictionary of country code to name
c_code_to_name = None
r_code_to_name = None
i_code_to_name = None
agri_data_df = None

data_columns = [
    #'yield', # Y
    # crop Wheat=15, Rice=27, Onion=403
    #'item_code',
    # region classification
    #'R_EA_P' = 1, # East Asia and Pacific (one-hot encoded)
    #'R_E_CA' = 2, # Europe and Central Asia (one-hot encoded)
    #'R_HI' = 3, # High Income is a region on its own (one-hot encoded)
    #'R_LAm_C' = 4, # Latin America and Caribbean (one-hot encoded)
    #'R_ME_NAf' = 5, # Middle East and North Africa (one-hot encoded)
    #'R_SA' = 6, # South Asia (one-hot encoded)
    #'R_SSAf' = 7, # Sub Saharan Africa (one-hot encoded)
    #'region_code',
    # income classification
    #'I_LI' = 1, # Low Income (one-hot encoded)
    #'I_LMI' = 2, # Low Medium Income (one-hot encoded)
    #'I_UMI' = 3, # Upper Medium Income (one-hot encoded)
    #'I_HI' = 4, # High Income (all high income regions belong here) (one-hot encoded)
    #'income_code',
    # fertilizer
    'F_N', # Nitrogen
    'F_P', # Phosphorus
    'F_K', # Potassium
    # land use
    'L_AL', # arable land (% total land)
    'L_PC', # permanent crop land (% total land)
    'L_PM', # permanent meadows (% of total land)
    'L_EI', # land equiped for irrigation (% of total land)
    #'Pest', # pesticide used (kg/ha) remove
    'W', # water used for agriculture (% total water used) Region Avg if na
    #'GDP', # GDP in USD - Remove for analysis
    'C', # Carbon (% by weight) Region Avg if na
    'country_name', # conuntry name
    'lt_1h',
    '1_2h',
    '2_5h',
    '5_10h',
    '10_20h',
    '20_50h',
    '50_1hh',
    '1h_2hh',
    '2h_5hh',
    '5h_1kh',
    'gt_1kh',
    'Wkr',
    'Trk'
]

def init():
    global c_code_to_name
    global agri_data_df
    global r_code_to_name
    global i_code_to_name
    prepare_data.load_countries()
    prepare_data.load_regions()
    prepare_data.load_income()
    c_code_to_name = prepare_data.c_code_to_name
    r_code_to_name = prepare_data.r_code_to_name
    i_code_to_name = prepare_data.i_code_to_name
    agri_data_df = DataFrame.from_csv(app_settings.get_data_file(input_file))
    agri_data_df['gt_1hh'] = agri_data_df['1h_2hh'] + \
        agri_data_df['2h_5hh'] + agri_data_df['5h_1kh'] + \
        agri_data_df['gt_1kh']

# plot the attribute we want to predict
def plot_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    s = get_series(df, 'yield', 'area_code')
    title='Yield for Wheat'
    plots.plot_bar_chart(s, c_code_to_name, title=title, kind='barh')
    plots.plot_histogram(s, title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    s = get_series(df, 'yield', 'area_code')
    title='Yield for Rice'
    plots.plot_bar_chart(s, c_code_to_name, title=title, kind='barh')
    plots.plot_histogram(s, title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    s = get_series(df, 'yield', 'area_code')
    title='Yield for Onion'
    plots.plot_bar_chart(s, c_code_to_name, title=title, kind='barh')
    plots.plot_histogram(s, title)
    
def plot_N_fertilizer_use_vs_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Nitrogen Fertilizer-use Vs Yield for Wheat'
    plots.plot_scatter(df, 'F_N', ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Nitrogen Fertilizer-use vs Yield for Rice'
    plots.plot_scatter(df, 'F_N', ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Nitrogen Fertilizer-use vs Yield for Onion'
    plots.plot_scatter(df, 'F_N', ['yield'], title=title)
    
def plot_P_fertilizer_use_vs_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Phosphate Fertilizer-use Vs Yield for Wheat'
    plots.plot_scatter(df, 'F_P', ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Phosphate Fertilizer-use vs Yield for Rice'
    plots.plot_scatter(df, 'F_P', ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Phosphate Fertilizer-use vs Yield for Onion'
    plots.plot_scatter(df, 'F_P', ['yield'], title=title)
    
def plot_K_fertilizer_use_vs_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Potassium Fertilizer-use Vs Yield for Wheat'
    plots.plot_scatter(df, 'F_K', ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Potassium Fertilizer-use vs Yield for Rice'
    plots.plot_scatter(df, 'F_K', ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Potassium Fertilizer-use vs Yield for Onion'
    plots.plot_scatter(df, 'F_K', ['yield'], title=title)
    
def plot_water_use_vs_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Water-use Vs Yield for Wheat'
    plots.plot_scatter(df, 'W', ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Water-use vs Yield for Rice'
    plots.plot_scatter(df, 'W', ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Water-use vs Yield for Onion'
    plots.plot_scatter(df, 'W', ['yield'], title=title)
    
def plot_land_equiped_for_irrigation_vs_yield():
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Land Equiped For Irrigation Vs Yield for Wheat'
    plots.plot_scatter(df, 'L_EI', ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Land Equiped For Irrigation vs Yield for Rice'
    plots.plot_scatter(df, 'L_EI', ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Land Equiped For Irrigation vs Yield for Onion'
    plots.plot_scatter(df, 'L_EI', ['yield'], title=title)
    
def plot_farm_size_vs_yield(farm_size):
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title=farm_size + ' Vs Yield for Wheat'
    plots.plot_scatter(df, farm_size, ['yield'], title=title)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title=farm_size + ' vs Yield for Rice'
    plots.plot_scatter(df, farm_size, ['yield'], title=title)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title=farm_size + ' vs Yield for Onion'
    plots.plot_scatter(df, farm_size, ['yield'], title=title)

def plot_boxplot(by, x_dict=None):
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Wheat by ' + str(by)
    plots.plot_box(df, columns=['yield'], by=by, title=title, x_dict=x_dict)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Rice ' + str(by)
    plots.plot_box(df, columns=['yield'], by=by, title=title, x_dict=x_dict)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Onion ' + str(by)
    plots.plot_box(df, columns=['yield'], by=by, title=title, x_dict=x_dict)

def plot_violinplot(by, x_dict=None):
    # get latest yield for wheat and print
    df = agri_data_df[(agri_data_df['item_code'] == 15) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Wheat by ' + str(by)
    plots.plot_violin(df, x_col_name=by, y_col_name='yield', title=title, x_dict = x_dict)
    # yield for rice
    df = agri_data_df[(agri_data_df['item_code'] == 27) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Rice ' + str(by)
    plots.plot_violin(df, x_col_name=by, y_col_name='yield', title=title, x_dict = x_dict)
    # yield for onion
    df = agri_data_df[(agri_data_df['item_code'] == 403) & (agri_data_df['year_code'] == 2015)]
    title='Yield for Onion ' + str(by)
    plots.plot_violin(df, x_col_name=by, y_col_name='yield', title=title, x_dict = x_dict)
    
def get_series(df, col_name, index_col_name = None, sort=True):
    s = df[col_name].copy()
    s.index = df[index_col_name]
    if sort:
        s.sort_values(inplace=True)
    return s

# always initialize the module when imported or run as main program
def run_all():
    init()
    plot_yield()
    plot_water_use_vs_yield()
    plot_land_equiped_for_irrigation_vs_yield()
    plot_farm_size_vs_yield('lt_1h')
    plot_farm_size_vs_yield('1_2h')
    plot_farm_size_vs_yield('2_5h')
    plot_farm_size_vs_yield('5_10h')
    plot_farm_size_vs_yield('10_20h')
    plot_farm_size_vs_yield('20_50h')
    plot_farm_size_vs_yield('50_1hh')
    plot_farm_size_vs_yield('gt_1hh')
    plot_farm_size_vs_yield('1h_2hh')
    plot_farm_size_vs_yield('2h_5hh')
    plot_farm_size_vs_yield('5h_1kh')
    plot_farm_size_vs_yield('gt_1kh')
    plot_boxplot(['region_code'], r_code_to_name)
    plot_boxplot(['income_code'], i_code_to_name)
    plot_boxplot(['region_code', 'income_code'])
    plot_violinplot('region_code', r_code_to_name)
    plot_violinplot('income_code', i_code_to_name)
    plot_N_fertilizer_use_vs_yield()
    plot_P_fertilizer_use_vs_yield()
    plot_K_fertilizer_use_vs_yield()
    
if __name__ == '__main__':
    run_all()
