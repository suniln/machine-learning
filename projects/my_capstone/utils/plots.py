# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from pandas.plotting import scatter_matrix
import seaborn as sns

def plot_agg_element(c_agg_df, item_code, xtick_dict, 
                     median_col_name, mean_col_name,
                     x_label, y_label, item_name, element):
    #mng = plt.get_current_fig_manager()
    #mng.window.showMaximized()
    plt.tight_layout()
    fig, axes = plt.subplots(2, 1)
    print(c_agg_df)
    median_df = (c_agg_df.loc[item_code][median_col_name]).sort_values(ascending=False)
    median_df.plot(ax=axes[0], kind='bar', title= 'Median ' + element + ' For ' + item_name)
    xtick_labels = [xtick_dict[c] for c in median_df.index]
    for i in range(len(xtick_labels)):
        if i % 2 == 1:
            xtick_labels[i] = ''
    axes[0].set_xticklabels(xtick_labels)
    axes[0].set_ylabel(y_label)
    axes[0].set_xlabel(x_label)
    mean_df = (c_agg_df.loc[item_code][mean_col_name]).sort_values(ascending=False)
    mean_df.plot(ax=axes[1], kind='bar', title= 'Mean ' + element + ' For ' + item_name)
    xtick_labels = [xtick_dict[c] for c in median_df.index]
    for i in range(len(xtick_labels)):
        if i % 2 == 1:
            xtick_labels[i] = ''
    axes[1].set_xticklabels(xtick_labels)
    axes[1].set_ylabel(y_label)
    axes[1].set_xlabel(x_label)
    plt.tight_layout()

def get_element_for_country_and_item(c_df, country_code, item_code, value_col_name):
    data = Series(
        c_df[(c_df['area_code'] == country_code) & 
                        (c_df['item_code'] == item_code)][value_col_name]
        )
    data.index = c_df[(c_df['area_code'] == country_code) &
                    (c_df['item_code'] == item_code)]['year_code']
    return data

def plot_element_for_item_over_time(c_df, seleted_country_codes, 
                            code_to_name, item_code, value_col_name, title,
                            marker = None):
    data = {}
    for c in seleted_country_codes:        
        data[code_to_name[c].lower()] = get_element_for_country_and_item(c_df, 
             c, item_code, value_col_name)
    print('data', data)
    DataFrame(data).plot(title=title, marker=marker)
 
# index of the df is the x axis
# code_to_name maps index value to text
def plot_stacked_bar_chart(df, code_to_name=None, title=None):
    #mng = plt.get_current_fig_manager()
    #mng.window.showMaximized()
    plt.tight_layout()
    fig,ax = plt.subplots(1,1)
    df.plot(ax=ax, kind='bar', stacked=True, alpha=0.5, title = title, rot=0)
    if code_to_name:
        ax.set_xticklabels([code_to_name[index] for index in df.index])
    ax.set_xlabel("country " + title)
    ax.legend(loc='left', ncol=5, mode='expand', borderaxespad=0.,
              bbox_to_anchor=(0., 1.02, 1., .102))
    plt.show()
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    """
    ax.plot(df, kind='bar', stacked=True, alpha=0.5, title = title)
    ax.set_xticklabels([code_to_name[index] for index in df.index], rotation=90)
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    plt.show()"""
    
# index of the df is the x axis
# code_to_name maps index value to text
def plot_bar_chart(df, code_to_name=None, title=None, kind='bar'):
    if code_to_name:
        df.index = [code_to_name[i] for i in df.index]
    fig,ax = plt.subplots(1,1)
    df.plot(kind=kind, title=title, ax=ax)
    
# y_cols is list of columns of max length 2
def plot_scatter(df, x_col, y_cols, title=None):
    ax = df.plot.scatter(x=x_col, y=y_cols[0], color='Red', s=80, title=title)
    if len(y_cols) > 1:
        df.plot.scatter(x=x_col, y=y_cols[1], color='DarkGreen', s=40, ax=ax, title=title)
        
#x and y need to be ndarray
def plot_scatter_from_series(x, y, x_label, y_label, title=None):
    fig, ax = plt.subplots()
    ax.scatter(x, y, edgecolors=(0, 0, 0))
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.suptitle(title)
    plt.show()
    
def plot_histogram(df, title=None):
    fig,ax = plt.subplots(1,1)
    df.plot.hist(ax=ax, title=title)
    
def plot_box(df, columns, by, title, x_dict = None):
    ax = df.boxplot(column=columns, by=by)
    if x_dict:
        x_vals = ax.get_xticklabels()
        ax.set_xticklabels(x_dict[int(t.get_text())] for t in x_vals)
    plt.suptitle(title)
    plt.show()
    
def plot_violin(df, x_col_name, y_col_name, title, x_dict = None):
    plt.figure()
    col_order = list(df[x_col_name].unique())
    ax = sns.violinplot(x=x_col_name, y=y_col_name, data=df, order=col_order)
    if x_dict:
        x_vals = ax.get_xticklabels()
        ax.set_xticklabels(x_dict[int(t.get_text())] for t in x_vals)
    plt.suptitle(title)
    plt.show()

def plot_scatter_matrix(df, title):
    scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.suptitle(title)
    plt.show()