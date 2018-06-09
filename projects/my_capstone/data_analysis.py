# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import operator
import os
import app_settings
import generate_train_test_sets
from utils import plots

# if False will generate and save the files
# else will used previously generated and saved files
use_saved_train_test_sets = True

def init():
    if os.path.exists(app_settings.result_file_name):
        os.remove(app_settings.result_file_name)
        
columns_x = [#'item_code', 
    'F_N', 
    'F_P', 
    'F_K', 
    'L_AL', 
    'L_PC', 
    #'L_PM',  This is negatively correlated with L_AL so is redundant
    'L_EI', 
    'W', 
    #'GDP', 
    'C', 
    'lt_1h', 
    '1_2h', 
    '2_5h',
    '5_10h', 
    '10_20h', 
    '20_50h', 
    '50_1hh', 
    'gt_1hh',
    'Wkr', 
    'Trk'
    ]

column_y_name = 'yield'
columns_y = [column_y_name]

def run_linear_reg(train_df, test_df, test_name=None):
    reg = linear_model.LinearRegression()
    reg.fit(train_df[columns_x], train_df[column_y_name])
    r2_train = reg.score(train_df[columns_x], train_df[column_y_name])
    coeff = reg.coef_
    intercept = reg.intercept_
    pred_train = reg.predict(train_df[columns_x])
    mse_train = mean_squared_error(pred_train, train_df[column_y_name])
    mae_train = mean_absolute_error(pred_train, train_df[column_y_name])
    r2 = reg.score(test_df[columns_x], test_df[columns_y])
    pred_test = reg.predict(test_df[columns_x])
    mse_test = mean_squared_error(pred_test, test_df[column_y_name])
    mae_test = mean_absolute_error(pred_test, test_df[column_y_name])
    print(test_name, 
          'r squared test:', round(r2,2), 
          'r squared train:', round(r2_train,2),
          'mse test:', round(np.sqrt(mse_test),2), 
          'mse train:', round(np.sqrt(mse_train),2),
          'mae_test:', round(mae_test,2), 
          'mae_train:', round(mae_train,2),
          'coeff:', coeff, 
          'intercept:', intercept)
    with open(app_settings.result_file_name, 'a') as file:
        file.write('Metrics for {0}\n'.format(test_name))
        file.write('------------------------\n')
        file.write('coeff: {0}\n'.format(coeff))
        file.write('intercept: {0}\n'.format(intercept))
        file.write('r squared test: {0:.2f}\n'.format(r2))
        file.write('r squared train: {0:.2f}\n'.format(r2_train))
        file.write('RMSE test : {0:.2f}\n'.format(np.sqrt(mse_test)))
        file.write('RMSE test  (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_test) * 100 / test_df[column_y_name].mean()))
        file.write('RMSE train: {0:.2f}\n'.format(np.sqrt(mse_train)))
        file.write('RMSE train (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_train) * 100 / train_df[column_y_name].mean()))
        file.write('RMAE test : {0:.2f}\n'.format(mae_test))
        file.write('RMAE test  (% of average yield): {0:.2f}\n'.format(
                mae_test * 100 / test_df[column_y_name].mean()))
        file.write('RMAE train: {0:.2f}\n'.format(mae_train))
        file.write('RMAE train (% of average yield): {0:.2f}\n'.format(
                mae_train * 100 / train_df[column_y_name].mean()))
        file.write('\n\n\n')
    return reg

def run_linear_reg_norm(train_df, test_df, test_name=None):
    reg = linear_model.LinearRegression(normalize=True)
    reg.fit(train_df[columns_x], train_df[column_y_name])
    r2_train = reg.score(train_df[columns_x], train_df[column_y_name])
    coeff = reg.coef_
    intercept = reg.intercept_
    pred_train = reg.predict(train_df[columns_x])
    mse_train = mean_squared_error(pred_train, train_df[column_y_name])
    mae_train = mean_absolute_error(pred_train, train_df[column_y_name])
    r2 = reg.score(test_df[columns_x], test_df[columns_y])
    pred_test = reg.predict(test_df[columns_x])
    mse_test = mean_squared_error(pred_test, test_df[column_y_name])
    mae_test = mean_absolute_error(pred_test, test_df[column_y_name])
    print(test_name, 
          'r squared test:', round(r2,2), 
          'r squared train:', round(r2_train,2),
          'mse test:', round(np.sqrt(mse_test),2), 
          'mse train:', round(np.sqrt(mse_train),2),
          'mae_test:', round(mae_test,2), 
          'mae_train:', round(mae_train,2),
          'coeff:', coeff, 
          'intercept:', intercept)
    with open(app_settings.result_file_name, 'a') as file:
        file.write('Metrics for {0}\n'.format(test_name))
        file.write('------------------------\n')
        file.write('coeff: {0}\n'.format(coeff))
        file.write('intercept: {0}\n'.format(intercept))
        file.write('r squared test: {0:.2f}\n'.format(r2))
        file.write('r squared train: {0:.2f}\n'.format(r2_train))
        file.write('RMSE test : {0:.2f}\n'.format(np.sqrt(mse_test)))
        file.write('RMSE test  (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_test) * 100 / test_df[column_y_name].mean()))
        file.write('RMSE train: {0:.2f}\n'.format(np.sqrt(mse_train)))
        file.write('RMSE train (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_train) * 100 / train_df[column_y_name].mean()))
        file.write('RMAE test : {0:.2f}\n'.format(mae_test))
        file.write('RMAE test  (% of average yield): {0:.2f}\n'.format(
                mae_test * 100 / test_df[column_y_name].mean()))
        file.write('RMAE train: {0:.2f}\n'.format(mae_train))
        file.write('RMAE train (% of average yield): {0:.2f}\n'.format(
                mae_train * 100 / train_df[column_y_name].mean()))
        file.write('\n\n\n')
    return reg

def run_linear_reg_standardized(train_df, test_df, test_name=None):
    scaler = StandardScaler()
    train_std_df = DataFrame(scaler.fit_transform(train_df[columns_x]), columns= columns_x)
    test_std_df = DataFrame(scaler.fit_transform(test_df[columns_x]), columns= columns_x)
    reg = linear_model.LinearRegression()
    reg.fit(train_std_df[columns_x], train_df[column_y_name])
    r2_train = reg.score(train_std_df[columns_x], train_df[column_y_name])
    coeff = reg.coef_
    intercept = reg.intercept_
    pred_train = reg.predict(train_std_df[columns_x])
    mse_train = mean_squared_error(pred_train, train_df[column_y_name])
    mae_train = mean_absolute_error(pred_train, train_df[column_y_name])
    r2 = reg.score(test_std_df[columns_x], test_df[columns_y])
    pred_test = reg.predict(test_std_df[columns_x])
    mse_test = mean_squared_error(pred_test, test_df[column_y_name])
    mae_test = mean_absolute_error(pred_test, test_df[column_y_name])
    print(test_name, 
          'r squared test:', round(r2,2), 
          'r squared train:', round(r2_train,2),
          'mse test:', round(np.sqrt(mse_test),2), 
          'mse train:', round(np.sqrt(mse_train),2),
          'mae_test:', round(mae_test,2), 
          'mae_train:', round(mae_train,2),
          'coeff:', coeff, 
          'intercept:', intercept)
    with open(app_settings.result_file_name, 'a') as file:
        file.write('Metrics for {0}\n'.format(test_name))
        file.write('------------------------\n')
        file.write('coeff: {0}\n'.format(coeff))
        file.write('intercept: {0}\n'.format(intercept))
        file.write('r squared test: {0:.2f}\n'.format(r2))
        file.write('r squared train: {0:.2f}\n'.format(r2_train))
        file.write('RMSE test : {0:.2f}\n'.format(np.sqrt(mse_test)))
        file.write('RMSE test  (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_test) * 100 / test_df[column_y_name].mean()))
        file.write('RMSE train: {0:.2f}\n'.format(np.sqrt(mse_train)))
        file.write('RMSE train (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_train) * 100 / train_df[column_y_name].mean()))
        file.write('RMAE test : {0:.2f}\n'.format(mae_test))
        file.write('RMAE test  (% of average yield): {0:.2f}\n'.format(
                mae_test * 100 / test_df[column_y_name].mean()))
        file.write('RMAE train: {0:.2f}\n'.format(mae_train))
        file.write('RMAE train (% of average yield): {0:.2f}\n'.format(
                mae_train * 100 / train_df[column_y_name].mean()))
        file.write('\n\n\n')
    return reg
    
def run_rf_reg(train_df, test_df, test_name=None, n_estimators=10, criterion='mse'):
    reg = RandomForestRegressor()
    reg.fit(train_df[columns_x], train_df[column_y_name])
    print(reg.score(train_df[columns_x], train_df[column_y_name]))
    r2_train = reg.score(train_df[columns_x], train_df[column_y_name])
    pred_train = reg.predict(train_df[columns_x])
    mse_train = mean_squared_error(pred_train, train_df[column_y_name])
    mae_train = mean_absolute_error(pred_train, train_df[column_y_name])
    r2 = reg.score(test_df[columns_x], test_df[columns_y])
    pred_test = reg.predict(test_df[columns_x])
    mse_test = mean_squared_error(pred_test, test_df[column_y_name])
    mae_test = mean_absolute_error(pred_test, test_df[column_y_name])
    print(test_name, 'r squared test:', round(r2,2), 'r squared train:', round(r2_train,2),
          'rmse test', round(np.sqrt(mse_test),2), 'rmse train', round(np.sqrt(mse_train),2),
          'rmae_test', round(mae_test,2), 'rmae_train', round(mae_train,2))
    print(columns_x)
    print(reg.feature_importances_)
    print(str([columns_x[i] for i in np.argsort(reg.feature_importances_)]))
    with open(app_settings.result_file_name, 'a') as file:
        file.write('Metrics for {0}\n'.format(test_name))
        file.write('------------------------\n')
        file.write('r squared test: {0:.2f}\n'.format(r2))
        file.write('r squared train: {0:.2f}\n'.format(r2_train))
        file.write('RMSE test : {0:.2f}\n'.format(np.sqrt(mse_test)))
        file.write('RMSE test  (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_test) * 100 / test_df[column_y_name].mean()))
        file.write('RMSE train: {0:.2f}\n'.format(np.sqrt(mse_train)))
        file.write('RMSE train (% of average yield): {0:.2f}\n'.format(
                np.sqrt(mse_train) * 100 / train_df[column_y_name].mean()))
        file.write('RMAE test : {0:.2f}\n'.format(mae_test))
        file.write('RMAE test  (% of average yield): {0:.2f}\n'.format(
                mae_test * 100 / test_df[column_y_name].mean()))
        file.write('RMAE train: {0:.2f}\n'.format(mae_train))
        file.write('RMAE train (% of average yield): {0:.2f}\n'.format(
                mae_train * 100 / train_df[column_y_name].mean()))
        file.write('Feature importance:\n{0}\n'.format(
                [columns_x[i] for i in np.argsort(reg.feature_importances_)]))
        file.write('\n\n\n')
    return reg
    
def plot_results(reg, x, y, title=None):
    predicted = reg.predict(x)
    # predicted is ndarray
    # convert y to ndarray
    plots.plot_scatter_from_series(y, predicted, 'observed', 'predicted',  title)

# feature selection
def find_significant_features(df, title):
    mi = mutual_info_regression(df[columns_x], df[column_y_name])
    column_info = dict(zip(columns_x, mi))
    sorted_cols = sorted(column_info.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_cols)
    scaler = StandardScaler()
    std_df = DataFrame(scaler.fit_transform(df[columns_x]), columns= columns_x)
    mi = mutual_info_regression(std_df[columns_x], df[column_y_name])
    column_info = dict(zip(columns_x, mi))
    sorted_cols_scaled = sorted(column_info.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_cols)
    with open(app_settings.result_file_name,'a') as file:
        #file.write('Significant columns for ' + title + ' dataset:\n')
        #file.write('{0}\n'.format(['{0}:{1:.2f}'.format(a, b) for (a,b) in sorted_cols]))
        file.write('Feature importance for ' + title + ' yield:\n')
        file.write('{0}\n'.format(['{0}:{1:.2f}'.format(a, b) for (a,b) in sorted_cols_scaled]))
        file.write('\n\n\n')
        
def print_data_summary(df, title):
    with open(app_settings.result_file_name, 'a') as file:
        file.write('Summary for ' + title + '\n')
        file.write('------------------------\n')
        file.write('shape: {0}\n'.format(str(df.shape)))
        file.write('number of countries: {0}\n'.format(len(df['area_code'].unique())))

def run_all():
    init()
    # do regression all items combined item
    #train, test = train_test_split(all_df, test_size=0.2, shuffle=True)
    #reg = run_linear_reg(train, test)
    #plot_results(reg, test[columns_x], test[columns_y], 'All items')
    
    # do regression by item
    if not use_saved_train_test_sets:
        generate_train_test_sets.generate_files()
        
    wheat_train, wheat_test = generate_train_test_sets.get_train_test_data('wheat')
    print_data_summary(wheat_train, 'Wheat train data')
    find_significant_features(wheat_train, 'Wheat')
    rice_train, rice_test = generate_train_test_sets.get_train_test_data('rice')
    print_data_summary(rice_train, 'Rice train data')
    find_significant_features(rice_train, 'Rice')
    onion_train, onion_test = generate_train_test_sets.get_train_test_data('onion')
    print_data_summary(onion_train, 'Onion train data')
    find_significant_features(onion_train, 'Onion')
    
    reg = run_linear_reg(wheat_train, wheat_test, 'Wheat (LR)')
    plot_results(reg, wheat_test[columns_x], wheat_test[column_y_name], 'Wheat (LR)')
    
    reg = run_linear_reg(rice_train, rice_test, 'Rice (LR)')
    plot_results(reg, rice_test[columns_x], rice_test[column_y_name], 'Rice (LR)')
    
    reg = run_linear_reg(onion_train, onion_test, 'Onion (LR)')
    plot_results(reg, onion_test[columns_x], onion_test[column_y_name], 'Onion (LR)')
    
    reg = run_linear_reg_norm(wheat_train, wheat_test, 'Wheat (LR-Normalize)')
    plot_results(reg, wheat_test[columns_x], wheat_test[column_y_name], 'Wheat (LR-Normalize)')
    
    reg = run_linear_reg_norm(rice_train, rice_test, 'Rice (LR-Normalize)')
    plot_results(reg, rice_test[columns_x], rice_test[column_y_name], 'Rice (LR-Normalize)')
    
    reg = run_linear_reg_norm(onion_train, onion_test, 'Onion (LR-Normalize)')
    plot_results(reg, onion_test[columns_x], onion_test[column_y_name], 'Onion (LR-Normalize)')
    
    scaler = StandardScaler()
    reg = run_linear_reg_standardized(wheat_train, wheat_test, 'Wheat (LR-Standardized)')
    wheat_test_std_df = DataFrame(scaler.fit_transform(wheat_test[columns_x]), columns= columns_x)
    plot_results(reg, wheat_test_std_df[columns_x], wheat_test[column_y_name], 'Wheat (LR-Standardized)')
    
    reg = run_linear_reg_standardized(rice_train, rice_test, 'Rice (LR-Standardized)')
    rice_test_std_df = DataFrame(scaler.fit_transform(rice_test[columns_x]), columns= columns_x)
    plot_results(reg, rice_test_std_df[columns_x], rice_test[column_y_name], 'Rice (LR-Standardized)')
    
    reg = run_linear_reg_standardized(onion_train, onion_test, 'Onion (LR-Standardized)')
    onion_test_std_df = DataFrame(scaler.fit_transform(onion_test[columns_x]), columns= columns_x)
    plot_results(reg, onion_test_std_df[columns_x], onion_test[column_y_name], 'Onion (LR-Standardized)')
    
    for c in ['mse', 'mae']:
        for n in [6, 8, 10, 12, 16, 20, 25, 30, 35, 40]:
            reg = run_rf_reg(wheat_train, wheat_test, 'Wheat (RF-n_est={0} {1})'.format(n, c), n_estimators= n)
            plot_results(reg, wheat_test[columns_x], wheat_test[column_y_name], 
                         'Wheat (RF-n_est={0} {1})'.format(n, c))
            
            reg = run_rf_reg(rice_train, rice_test, 'Rice (RF-n_est={0} {1})'.format(n, c))
            plot_results(reg, rice_test[columns_x], rice_test[column_y_name], 
                         'Rice (RF-n_est={0} {1})'.format(n, c))
            
            reg = run_rf_reg(onion_train, onion_test, 'Onion (RF-n_est={0} {1})'.format(n, c))
            plot_results(reg, onion_test[columns_x], onion_test[column_y_name], 
                         'Onion (RF-n_est={0} {1})'.format(n, c))
if __name__ == '__main__':           
    run_all()
