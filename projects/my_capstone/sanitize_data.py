# -*- coding: utf-8 -*-
import operator
import app_settings
from pandas import Series, DataFrame
import prepare_data
from utils import plots

out_file_name = app_settings.final_agri_file_name

# In this module we sanitize the data:
# remove outliers, fillna
all_columns = ['area_code', 
    'year_code', 
    'yield', 
    # crop Wheat=15, Rice=27, Onion=403
    'item_code',
    # region classification
    #'R_EA_P' = 1, # East Asia and Pacific (one-hot encoded)
    #'R_E_CA' = 2, # Europe and Central Asia (one-hot encoded)
    #'R_HI' = 3, # High Income is a region on its own (one-hot encoded)
    #'R_LAm_C' = 4, # Latin America and Caribbean (one-hot encoded)
    #'R_ME_NAf' = 5, # Middle East and North Africa (one-hot encoded)
    #'R_SA' = 6, # South Asia (one-hot encoded)
    #'R_SSAf' = 7, # Sub Saharan Africa (one-hot encoded)
    'region_code',
    # income classification
    #'I_LI' = 1, # Low Income (one-hot encoded)
    #'I_LMI' = 2, # Low Medium Income (one-hot encoded)
    #'I_UMI' = 3, # Upper Medium Income (one-hot encoded)
    #'I_HI' = 4, # High Income (all high income regions belong here) (one-hot encoded)
    'income_code',
    # fertilizer
    'F_N', # Nitrogen
    'F_P', # Phosphorus
    'F_K', # Potassium
    # land use
    'L_AL', # arable land (% total land)
    'L_PC', # permanent crop land (% total land)
    'L_PM', # permanent meadows (% of total land)
    'L_I', # irrigated land (% of total land) (REMOVE)
    'L_EI', # land equiped for irrigation (% of total land)
    'Pest', # pesticide used (kg/ha) remove
    'W', # water used for agriculture (% total water used) Region Avg if na
    'GDP', # GDP in USD - Remove for analysis
    'Enrg', # Energy used (% total energy used) (REMOVE)
    'S_Ero', # Soil erosion (GLASOD degrees) (REMOVE)
    'S_Deg', # Soil degradation (GLASOD degrees) (REMOVE)
    'C', # Carbon (% by weight) Region Avg if na
    'country_name', # conuntry name
    'lt_1h', # Region Avg if na
    '1_2h', # Region Avg if na
    '2_5h', # Region Avg if na
    '5_10h', # Region Avg if na
    '10_20h', # Region Avg if na
    '20_50h', # Region Avg if na
    '50_100h', # Region Avg if na
    '100_200h', # Region Avg if na
    '200_500h', # Region Avg if na
    '500_1000h', # Region Avg if na
    'gt_1000h', # Region Avg if na
    'Wkr',
    'Trk']

data_columns = [    
    # fertilizer
    'F_N', # Nitrogen
    'F_P', # Phosphorus
    'F_K', # Potassium
    # land use
    'L_AL', # arable land (% total land)
    'L_PC', # permanent crop land (% total land)
    'L_PM', # permanent meadows (% of total land)
    'L_I', # irrigated land (% of total land) (REMOVE)
    'L_EI', # land equiped for irrigation (% of total land)
    'Pest', # pesticide used (kg/ha)
    'W', # water used for agriculture (% total water used) Region Avg if na
    #'GDP', # GDP in USD - Remove for analysis
    'Enrg', # Energy used (% total energy used) (REMOVE)
    'S_Ero', # Soil erosion (GLASOD degrees) (REMOVE)
    'S_Deg', # Soil degradation (GLASOD degrees) (REMOVE)
    'C', # Carbon (% by weight) Region Avg if na
    'lt_1h', # Region Avg if na
    '1_2h', # Region Avg if na
    '2_5h', # Region Avg if na
    '5_10h', # Region Avg if na
    '10_20h', # Region Avg if na
    '20_50h', # Region Avg if na
    '50_1hh', # Region Avg if na
    '1h_2hh', # Region Avg if na
    '2h_5hh', # Region Avg if na
    '5h_1kh', # Region Avg if na
    'gt_1kh', # Region Avg if na
    'Wkr',
    'Trk']

scatter_matrix_cols = [    
    'yield', 
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
    'GDP', # GDP in USD - Remove for analysis
    'C', # Carbon (% by weight) Region Avg if na
    'Wkr',
    'Trk'
    ]

scatter_matrix_colsx= [    
    'yield', 
    'GDP', # Including GDP just to see if it relates to land size
    'lt_1h', # Region Avg if na
    '1_2h', # Region Avg if na
    '2_5h', # Region Avg if na
    '5_10h', # Region Avg if na
    '10_20h', # Region Avg if na
    '20_50h', # Region Avg if na
    '50_1hh', # Region Avg if na
    '1h_2hh', # Region Avg if na
    '2h_5hh', # Region Avg if na
    '5h_1kh', # Region Avg if na
    'gt_1kh', # Region Avg if na
    ]

farm_size_columns = [    
    'lt_1h', # Region Avg if na
    '1_2h', # Region Avg if na
    '2_5h', # Region Avg if na
    '5_10h', # Region Avg if na
    '10_20h', # Region Avg if na
    '20_50h', # Region Avg if na
    '50_1hh', # Region Avg if na
    '1h_2hh', # Region Avg if na
    '2h_5hh', # Region Avg if na
    '5h_1kh', # Region Avg if na
    'gt_1kh', # Region Avg if na
    ]

# country id and list of columns with no data
country_col_d = {}
# col name and list of countries with no data
col_country_d = {}

# eliminated countries
eliminated_countries = set()

# eliminated columns
eliminated_columns = set()

# significant columns
columns_with_data = None
# significant countries
countries_with_data = None

all_df = None # should be set by calling code
pruned_df = None # we will build this
min_max_year_df = None
c_code_to_name = None # country codes to name dictionary

# eliminate countries which are missing data for more than 5 columns
missing_data_threshold_per_country = 5
# eiliminate columns which are missing data for more than 15 countries
missing_country_threshold_per_column = 15
# this function gets the max/min year_code for which
# column has values
def get_max_min_year_with_values(column):
    all_df[~all_df['F_N'].isnull()].groupby('area_code')['year_code'].agg(['count', 'min', 'max'])
    
# columns is iterable
def fill_na_within_time_series(columns):
    for c in all_df['area_code'].unique():
        # wheat
        replace_values(
            all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 15), columns].interpolate(),
            columns)
        # rice
        replace_values(
            all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 27), columns].interpolate(),
            columns)
        # onion
        replace_values(
            all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 403), columns].interpolate(),
            columns)
        
def fill_na_at_ends_of_time_series(columns):
    for c in all_df['area_code'].unique():
        # wheat
        replace_values(all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 15), 
                                  columns].fillna(method='ffill').fillna(method='bfill'), columns)
        # rice
        replace_values(all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 27), 
                                  columns].fillna(method='ffill').fillna(method='bfill'), columns)
        # onion
        replace_values(all_df.loc[(all_df['area_code'] == c) & (all_df['item_code'] == 403), 
                              columns].fillna(method='ffill').fillna(method='bfill'), columns)

def replace_values(df, columns):
    for i in df.index:
        for col in columns:
            all_df.loc[i, col] = df.loc[i][col]
    
def save_data():
    all_df.to_csv(app_settings.get_data_file(out_file_name))

def fill_na():
    global all_df
    # based on output of this we know we have data between 2002 and 2015
    get_max_min_year_with_values('F_N')
    # get data only for years 2002 - 2015
    all_df = all_df[all_df['year_code'].isin(range(2002, 2016))]
    all_df = all_df[~all_df['area_code'].isin(eliminated_countries)]
    all_df = all_df.drop(eliminated_columns, axis=1)
    # fill na for fertilizer data (only inner missing values)
    columns = set(data_columns) - set(eliminated_columns)
    fill_na_within_time_series(columns) # ['F_N', 'F_P', 'F_K', 'L_AL', 'L_PC', 'L_PM', 'L_I', 'L_EI']
    # land use does not change dramatically year over year
    # it is OK to ffill and bfill these values
    fill_na_at_ends_of_time_series(columns) #['L_AL', 'L_PC', 'L_PM', 'L_I', 'L_EI']

def drop_na():
    all_df.dropna(inplace=True)
    
# needs df grouped by area_code
# we set max and min year as 2018 if column has no data for the country
# this provides a smaller range on y-axis when we plot graph
def get_max_min_year_for_columns(group, columns):
    d = {}
    for col in columns:
        if group[col].first_valid_index():
            d[col + '_min'] = group.loc[group[col].first_valid_index()]['year_code']
        else:
            d[col + '_min'] = 2018
        if group[col].last_valid_index():
            d[col + '_max'] = group.loc[group[col].last_valid_index()]['year_code']
        else:
            d[col + '_max'] = 2018
    return Series(d)

def assess_data_completion(plot_max_min_year_for_columns=False, plot_missing_data=False):
    # we get the max and min years for which we have data for each column
    # in each country and decide which columns to drop because of
    # insufficient or sparse data
    # plot number of countries which do not have data for each column
    # plot number of columns missing for each country
    global min_max_year_df
    global country_col_d
    global col_country_d
    global eliminated_countries
    global eliminated_columns
    
    country_eliminated = False
    col_eliminated = False
    
    df = prepare_data.read_merged_agri_data(one_hot_encoded=False)
    columns = df.columns.drop('country_name').drop('item_code').drop('region_code').drop('income_code')
    
    print_missing_data_count(df)
    
    # get data only for one crop
    df = df[df['item_code'] == 15] # wheat
    # group by country code
    grouped = df.groupby(['area_code'])
    # get min, max year for each column for which we have data
    min_max_year_df = grouped.apply(get_max_min_year_for_columns, columns)
    min_max_year_df['area_code'] = min_max_year_df.index
    
    # LOOP identifies countries and columns to eliminate
    # because of insufficient data
    country_eliminated = True
    col_eliminated = True
    country_col_d = {}
    col_country_d = {}
    while country_eliminated or col_eliminated:
        for col in columns:
            if col in farm_size_columns:
                continue
            if col in eliminated_columns:
                continue
            
            col_min = col + '_min'
            col_max = col + '_max'
            col_country_d[col] = set()
            if plot_max_min_year_for_columns:
                plots.plot_scatter(min_max_year_df, 'area_code', [col_min, col_max])
            # for each column list countries where we do not have any data
            # min_year == max_year == 2018 for missing data
            for c in  min_max_year_df[(min_max_year_df[col_min] == 2018) & 
                 (min_max_year_df[col_max] == 2018)]['area_code']:
                country_col_d[c] = country_col_d.get(c,set())
                country_col_d[c].add(col)
                col_country_d[col].add(c)
                
        country_col_count_d = {}
        for k in country_col_d:
            country_col_count_d[k] = len(country_col_d[k])
            print(c_code_to_name[k], len(country_col_d[k]), sorted(country_col_d[k]))

        col_country_count_d = {}
        for k in col_country_d:
            col_country_count_d[k] = len(col_country_d[k])
            print(k, len(col_country_d[k]), 
                  sorted([c_code_to_name[c] for c in col_country_d[k]]))
            
        country_eliminated = False
        col_eliminated = False
        country_codes = sorted(country_col_count_d.items(), key=operator.itemgetter(1), reverse=True)
        
        for cc in country_codes:
            c_code = cc[0]
            if c_code in eliminated_countries:
                continue
            if country_col_count_d[c_code] > missing_data_threshold_per_country:
                eliminated_countries.add(c_code)
                country_eliminated = True
                #drop the country
                df = df[df['area_code'] != c_code]
                break
            
        if not country_eliminated:
            cols = sorted(col_country_count_d.items(), key=operator.itemgetter(1), reverse=True)
            for cc in cols:
                col_name = cc[0]
                if col_name in eliminated_columns:
                    continue
                if col_country_count_d[col_name] > missing_country_threshold_per_column:
                    eliminated_columns.add(col_name)
                    col_eliminated = True
                    #drop the column
                    df = df.drop(col_name, axis=1)
                    break

def plot_missing_data():
    # looking at the charts we decide to eliminate columns which is missing data
    # for 15 countries or more
    missing_data_by_country_df = \
        DataFrame.from_dict({k : len(country_col_d[k]) 
            for k in country_col_d.keys() if len(country_col_d[k]) > 0}, orient='index')
    missing_data_by_country_df.columns = ['Number of Columns with null values']
    plots.plot_bar_chart(missing_data_by_country_df, c_code_to_name,
        'Number of columns with missing values')
            
    # looking at the chart we decide to eliminate countries that are missing
    # data for more than 5 columns
    missing_data_by_col_df = \
        DataFrame.from_dict({k: len(col_country_d[k]) 
            for k in col_country_d.keys() if len(col_country_d[k]) > 0}, orient='index')
    missing_data_by_col_df.columns = ['Number of Countries with null value']
    plots.plot_bar_chart(missing_data_by_col_df, None,
        'Number of Countries with missing value')
    

def print_missing_data_count(df):
    missing_df = df[(df['year_code'] == 2015) & (df['item_code'] == 15)].isnull().sum(axis=0).reset_index()
    missing_df.columns = ['column_name', 'missing_count']
    missing_df = missing_df[missing_df['missing_count'] > 0]
    print(missing_df)

def plot_scatter_matrix():
    # plot correlation matrix
    plots.plot_scatter_matrix(all_df[all_df['item_code'] == 15][scatter_matrix_cols], 'All Regions - Non Farm Size')
    """
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_EA_P')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 2)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_E_CA')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 3)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_HI')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 4)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_LAm_C')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 5)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_ME_NAf')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_SA')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_cols].mean(), 'R_SSAf')
    """
    
def plot_scatter_matrix_land_area():
    # plot correlation matrix
    plots.plot_scatter_matrix(all_df[all_df['item_code'] == 15][scatter_matrix_colsx], 'All Regions - Farm Size')
    """
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_EA_P')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 2)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_E_CA')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 3)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_HI')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 4)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_LAm_C')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 5)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_ME_NAf')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_SA')
    plots.plot_scatter_matrix(
        all_df[(all_df['item_code'] == 15) & (all_df['region_code'] == 1)].groupby(['area_code'])[scatter_matrix_colsx].mean(), 'R_SSAf')
    """
    
def plot_scatter_matrix_all_fields():
    # plot correlation matrix
    # final columns
    final_columns = [d for d in data_columns if d not in eliminated_columns]
    plots.plot_scatter_matrix(all_df[all_df['item_code'] == 15][final_columns], 'All Regions - All Fields')
    
def check_region_affinity_of_data(columns):
    pass

def init():
    global all_df
    global c_code_to_name
    if prepare_data.c_code_to_name is None:
        prepare_data.load_countries()
    all_df = prepare_data.read_merged_agri_data(one_hot_encoded=False)
    c_code_to_name = prepare_data.c_code_to_name

def print_data_summary():
    print('Final columns count=', len(all_df.columns))
    print(all_df.columns)
    final_countries = [(c, c_code_to_name[c]) for c in all_df['area_code'].unique()]
    print('Final countries count=', len(final_countries))
    print(final_countries)
    
def sanitize_all():
    init()
    # this will remove countries and columns for which
    # we do not have enough data
    assess_data_completion()
    plot_missing_data()
    # based on previous function we know that
    # eliminated countries are: [41, 256, 273, 213, 209, 201, 116]
    # eliminated columns are: ['L_I', 'S_Ero', 'S_Deg', 'Enrg']
    #eliminated_countries = [41, 256, 273, 213, 209, 201, 116]
    #eliminated_columns = ['L_I', 'S_Ero', 'S_Deg', 'Enrg']
    # pesticide data is sparse and suspect
    # We do not have pesticide data for Lebanon, Namibia, Uganda, Ivory Coast, 
    # Vietnam, Philippines
    # Also exporting countries have an incentive to not report use of pesticide
    # This eliminating pesticide
    eliminated_columns.add('Pest')
    fill_na()
    # too risky to use region or income averages
    # for countries where some data is missing
    # I will just drop na and use data for the countries remaining
    # this will still have some representation from each region
    # and income category
    drop_na()
    save_data()
    plot_scatter_matrix()
    plot_scatter_matrix_land_area()
    plot_scatter_matrix_all_fields()
    print_data_summary()
    
if __name__ == '__main__':
    sanitize_all()