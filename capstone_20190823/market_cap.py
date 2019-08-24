#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 18:29:40 2019

@author: winz
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#path = 'C:\\Users\\K\\AIDeepDiveMaterials\\'
path = '/Users/winz/Development/aideepdive/notebook/capstone_20190823/'

# Ticker, Total Assets, Number of Employees, Market Capitalization, Total Number of Transactions, Average Transaction Value

## 1. Create a DataFrame based on the guidance above. Don't forget to drop duplicates from dataset (b). Extra credit: Add a variable for the Total Value of Merger/Acquisition Transactions.
# df1 Columns: Index(['Name', 'Ticker', 'TotalAssets', 'TotalRevenue', 'GeographicSegments', 'PrimarySector'], dtype='object')
df1 = pd.read_csv(path+'SPTSXComposite.csv')
df1 = df1.set_index('Ticker')

# df2 Columns: Index(['Ticker', 'Name', 'MarketCapitalization', 'NumberEmployees'], dtype='object')
df2 = pd.read_csv(path+'SPTSXCap_Employees.csv')

# drop duplicates and set_index
df2 = df2.drop_duplicates(keep='first')
df2 = df2.set_index('Ticker')

# Columns: Index(['Date', 'Ticker', 'TransactionType', 'TransactionValue'], dtype='object')
df3 = pd.read_csv(path+'SP_Transactions.csv')

# get total transactions and average transaction values
dfCountMean = df3.groupby('Ticker').agg({'TransactionValue': ['count', 'mean']})
dfCountMean.columns = ["_".join(x) for x in dfCountMean.columns.ravel()]

# start joining dataframes
dfMarketCap = df1.join(df2, rsuffix='2')
dfMarketCap = dfMarketCap.join(dfCountMean)

# drop columns not needed
dfMarketCap = dfMarketCap.drop(['Name', 'Name2', 'TotalRevenue', 'GeographicSegments', 'PrimarySector'], axis=1)


## 2. Perform high level data validation - assess whether the range of each variable is reasonable, based on your intuition.
dfMarketCap.describe().round()

def desc_and_hist_columns(df):
    cols = list(df.columns)
    type(cols)
    for c in cols:
        print(df[[c]].describe().round())
        df[[c]].plot.hist()

desc_and_hist_columns(dfMarketCap)

## 3. Identify any rows/observations containing NaN or null values. Handle them as you see fit. Hint: If a company does not appear in the transactions dataset, it is because it closed no transactions during the relevant time period. Keep track of the ticker number of any observations that were removed or altered. 
dfMarketCap.isna().any()

# change NaN counts and means to 0
dfMarketCap[['TransactionValue_count', 'TransactionValue_mean']] = dfMarketCap[['TransactionValue_count', 'TransactionValue_mean']].fillna(0)


## 4. Consider the histogram of Market Capitalization. What does it tell you? Extra credit: Consider and apply an appropriate transformation to the Market Capitalization variable.
dfMarketCap.MarketCapitalization.plot.hist()

# apply log to dfMarketCap
dfMarketCap_log = np.log(dfMarketCap.replace(0, np.nan))
dfMarketCap_log.MarketCapitalization.plot.hist()

## 5. Explore the relationships between Market Capitalization and the other variables using scatter plots and a correlation matrix. Are the relationships strong or weak, positive or negative, linear or not? 
dfMarketCap.corr()
dfMarketCap_log.corr()

# show scatter plots
def show_scatterplots(df, title):
    for c1 in cols:
        for c2 in cols[cols.index(c1):]:
            if (c1 != c2):
                df.plot.scatter(c1, c2)
                plt.title(title) # interfaces with matplotlib
                plt.show()

show_scatterplots(dfMarketCap, 'Before Transformation')
show_scatterplots(dfMarketCap_log, 'After Transformation')

## 6. Save the cleaned DataFrame as a csv or excel file (df.to_csv(path) or df.to_excel(path)). (Create a new directory for your outputs/reports)
dfMarketCap.to_csv(path+'/output/MarketCap.csv')
dfMarketCap_log.to_csv(path+'/output/MarketCap_transformed.csv')
