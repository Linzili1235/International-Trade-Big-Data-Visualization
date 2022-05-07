# This file is for ploting linked graphs
# import packages
import os
import altair as alt
import pandas as pd
import numpy as np
from pyparsing import empty
from altair_saver import save

os.chdir("/Users/linzili1235/Desktop/graduate/503/project")

file_list = os.listdir('proj_data')
# keep only import data
file_name = [s for s in file_list if 'import' in s]

os.chdir('proj_data')


def data_preparation(name):
    col_list = ['Year', 'Partner', 'Commodity Code',
                'Commodity', 'Trade Value (US$)']
    df = pd.read_csv(name, usecols=col_list)
    df.columns = ['Year',
                  'Partner', 'Commodity_Code',
                  'Commodity', 'Trade_Value']
    df['Str_Len'] = df['Commodity_Code'].map(str).apply(len)
    # only keep the major product types
    df_less = df.loc[df['Str_Len'] == 2]
    df_world = df_less.loc[df_less['Partner'] != 'World']
    df_need = df_world.groupby(['Year', 'Partner', 'Str_Len'], as_index=False)[
        'Trade_Value'].sum()
    df_need = df_need.drop('Str_Len', axis=1)
    return df_need


df1 = data_preparation(file_name[0])
df2 = data_preparation(file_name[1])
df3 = data_preparation(file_name[2])
df4 = data_preparation(file_name[3])
df5 = data_preparation(file_name[4])

# find top 10 import country and get their trade_value every year


def get_top10(df1, df2, df3, df4, df5):
    df_whole = pd.concat([df1, df2, df3, df4, df5], axis=0)
    df_sum = df_whole.groupby(['Partner'], as_index=False)['Trade_Value'].sum()
    df_order = df_sum.sort_values(by=['Trade_Value'], ascending=False)
    n_countries = df_order['Partner'][0:10].tolist()
    df_countries = df_whole.loc[df_whole['Partner'].isin(n_countries)]
    return df_countries


df_need = get_top10(df1, df2, df3, df4, df5)

# EU countries should be combined together
EU = ['Germany', 'France', 'Belgium', 'Ireland', 'Italy']
df_EU = df_need.loc[df_need['Partner'].isin(EU)]

df_EU = df_EU.groupby(['Year'], as_index=False)['Trade_Value'].mean()

df_EU['Partner'] = ['EU_Country']*len(df_EU)
df_nEU = df_need.loc[~df_need['Partner'].isin(EU)]
df_nEU = df_nEU.loc[df_nEU['Partner'] != 'Indonesia']
df_final = pd.concat([df_EU, df_nEU], axis=0)
df_final['Trade_Value'] = df_final['Trade_Value'].div(10000000000)
df_final['Year'] = pd.to_datetime(df_final['Year'], format='%Y-%m-%d')
df_final

df_final = df_final.reset_index()
df_final
# Exchange data
# https://fred.stlouisfed.org/
os.chdir("/Users/linzili1235/Desktop/graduate/503/project")

file_list = os.listdir('exchange_data')
country_name = [s.rsplit('.', 1)[0] for s in file_list]
os.chdir('exchange_data')


def exchange_data(file_list):
    start_date = '2016-01-01'
    end_date = '2020-12-01'
    df1 = pd.read_csv(file_list[0])
    df1.columns = ['Time', 'Exchange_Rate']
    df1['Time'] = df1['Time'].str.slice(stop=7)
    df1 = df1.groupby(['Time'], as_index=False)['Exchange_Rate'].max()
    df1['Time'] = pd.to_datetime(df1['Time'])
    mask1 = (df1['Time'] >= start_date) & (df1['Time'] <= end_date)
    df1 = df1.loc[mask1].reset_index()
    df1['Partner'] = [country_name[0]]*len(df1)
    for i in range(1, len(file_list)):
        df = pd.read_csv(file_list[i])
        df.columns = ['Time', 'Exchange_Rate']
        df['Time'] = df['Time'].str.slice(stop=7)
        df = df.groupby(['Time'], as_index=False)['Exchange_Rate'].max()
        df['Time'] = pd.to_datetime(df['Time'])
        df['Partner'] = [country_name[i]]*len(df)
        df1 = pd.concat([df1, df], axis=0)
    return df1


df_exchange = exchange_data(file_list)
# Plot
# base = alt.Chart(df_exchange).encode(

# )
selector = alt.selection_interval(empty='all', fields=['Partner'])
color_scale = alt.Scale(domain=country_name, scheme='category10')
base = alt.Chart().properties(
    width=250,
    height=250
).add_selection(selector)

lines = alt.Chart(df_exchange).mark_line().encode(
    alt.X('Time:T', axis=alt.Axis(title='Time(monthly)',
                                  titleColor='#1f77b4')),
    alt.Y('Exchange_Rate:Q', axis=alt.Axis(title='Exchange_Rate(1 dollar)',
                                           titleColor='seagreen')),
    color=alt.condition(selector,
                        'Partner:N',
                        alt.value('lightgray'),
                        scale=color_scale))
lines
hists = alt.Chart(df_final).mark_bar(size=25).encode(
    alt.X('Year:Q', bin=True,
          axis=alt.Axis(title='Time(yearly)',
                        titleColor='#1f77b4')),
    alt.Y('Trade_Value:Q', axis=alt.Axis(title='Trade_Value(US$ billions)',
                                         titleColor='seagreen'), stack=None),
    color=alt.Color('Partner:N',
                    scale=color_scale)).transform_aggregate(
    mean_acc='mean(Trade_Value)',
    groupby=["Year"]
).transform_filter(selector)
chart = lines | hists
chart.save('chart.html')
