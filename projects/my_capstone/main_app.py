# -*- coding: utf-8 -*-
import pandas as pd
import prepare_data
import sanitize_data
import data_exploration
import data_analysis

# load and merge all data from FAO and other sources 
# http://www.fao.org/faostat/en/#home
# data bulk downloaded and saved in data folder
# merge all data and write to csv file
prepare_data.enable_charts = False # set this to true to get charts for all agri datasets
prepare_data.load_and_merge_all_data()
# remove countries and fields with insufficient data
# fill na where appropriate
sanitize_data.sanitize_all()
# plot all kinds of graphs to explore the data
data_exploration.run_all()
# data analysis
data_analysis.run_all()