import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import time
import datetime


#location for all the files
os.chdir(r'C:\Users\komsi\Desktop\Projects\TwitterAPI')

# load the data from the twitter API
lc_df = pd.read_csv(r'C:\Users\komsi\Desktop\Projects\TwitterAPI\lc.csv') # first data , for Little Caesars
ms_df = pd.read_csv(r'C:\Users\komsi\Desktop\Projects\TwitterAPI\maesrto.csv') # Maestro Pizza


def total_interactions_column(df):
    ''' create new column for total interactions = retweets and likes '''

    df['total_interactions'] = df['retweet_count']+df['favorite_count']

total_interactions_column(lc_df)
total_interactions_column(ms_df)


def dates_column(df):
    ''' add a new date column that has the date as a datetime object '''
    dates = []
    for date in df['created_at']:
        date_as_datetime_opj = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        dates.append(date_as_datetime_opj)

    df['dates'] = dates



dates_column(lc_df)
dates_column(ms_df)

# create new dataframe that has only the tweets from the year 2020
lc_df_2020 = lc_df[lc_df['dates'] >= '2020']
ms_df_2020 = ms_df[ms_df['dates'] >= '2020']

# calulcate the sum and the average of the interactions in 2020
lc_interaction = lc_df_2020['total_interactions'].sum()
lc_interaction_avg = lc_interaction/len(lc_df_2020['total_interactions'])
ms_interaction = ms_df_2020['total_interactions'].sum()
ms_interaction_avg = ms_interaction/len(ms_df_2020['total_interactions'])


print('Little Caesars in 2020 tweeted ' , len(lc_df_2020['total_interactions']) , 'tweets\nand the Number of interaction in 2020 = ', lc_interaction,' Retweets and likes')
print('With an average of ', lc_interaction_avg ,'interaction Per tweet')

print('\n\nMaestro Pizza in 2020 tweeted ' , len(ms_df_2020['total_interactions']) , 'tweets\nand the Number of interaction in 2020 = ', ms_interaction ,' Retweets and likes')
print('With an average of ', ms_interaction_avg ,'interaction Per tweet')


# combine the two dataframes into one so we can plot them
combined_df = pd.concat([lc_df_2020.assign(dataset='Little Caesars'),ms_df_2020.assign(dataset='Maestro Pizza')],ignore_index=False,keys=['Little Caesars','Maestro Pizza'])
# new column for the hour the tweets was published at
combined_df['hour'] = combined_df['dates'].dt.hour


x_ticks_hours = [ i for i in range(0,24)]
x_ticks_months = [ i for i in range(1,13)]
x_ticks_days = [ i for i in range(1,32)]


sns.set_style("whitegrid") # optional style

# hours plot
hours_plot = sns.relplot(x='hour',y='total_interactions',data=combined_df,kind='line',hue='dataset',ci=None)
hours_plot.fig.suptitle('Interaction average for each hour')
hours_plot.set(ylim=(0,None),xticks=x_ticks_hours)


# days plot
days_plot = sns.relplot(x=combined_df['dates'].dt.day,y='total_interactions',data=combined_df,kind='line',hue='dataset',ci=None)
days_plot.fig.suptitle('Interaction average for each day')
days_plot.set(ylim=(0,None),xticks=x_ticks_days)

# months plot

months_plot = sns.relplot(x=combined_df['dates'].dt.month,y='total_interactions',data=combined_df,kind='line',hue='dataset',ci=None)
months_plot.fig.suptitle('Interaction average for each month')
months_plot.set(ylim=(0,None),xticks=x_ticks_months)

# number of tweets for each hour
# due some error I have to call plt.figure() to show the final properly
plt.figure()
tweets_each_hour = sns.countplot(x='hour',data=combined_df,hue='dataset')
tweets_each_hour.set_title('Number of tweets each hour')


plt.show()