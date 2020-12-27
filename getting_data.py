import pandas as pd
import json
import tweepy
import os
import time
import webbrowser


#location for the files
os.chdir(r'C:\Users\komsi\Desktop\Projects\TwitterAPI')

# first: twitter authentications

access_token = "--"
access_token_secret = "--"
consumer_key = "--"
consumer_secret = "--"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

redirect_url = auth.get_authorization_url()

api = tweepy.API(auth)


def extract_timeline_as_df(user):
    ''' This function will take the user name as a string and return its timeline(tweets) as a dataframe '''
    col = set()
    tweets_data = []
    user_timeline = tweepy.Cursor(api.user_timeline, id=user, include_rts=False, exclude_replies=True).items()
    user = api.get_user(user)
    for status in user_timeline:
        status_dict = dict(vars(status))
        single_tweet_data = {}
        for key in status_dict.keys():
            single_tweet_data[key] = status_dict[key]
            col.add(key)

        tweets_data.append(single_tweet_data)

    col_list = list(col)
    df = pd.DataFrame(tweets_data, columns=col_list)
    return df


# first user
lc_df = extract_timeline_as_df('lc_saudi')
lc_df.to_csv('lc_saudi.csv') # save it as csv

# second user
ms_df = extract_timeline_as_df('MaestroPizzaKSA')
ms_df.to_csv('MaestroPizzaKSA.csv') # save it as csv

