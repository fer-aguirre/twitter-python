import tweepy as tw
import pandas as pd
import re

def main():

    # Oauth keys
    consumer_key = '*****'
    consumer_secret = '*****'
    access_key = '*****'
    access_secret = '*****'

    # Authentication with Twitter
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    # API
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Select twitter username
    username = '@*****'

    # Query method using parameters
    tweets = tw.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended', exclude_replies=False, include_rts=False).items()

    # Pulling information from tweets iterable object
    tweets_list = [[tweet.full_text, tweet.created_at, tweet.id_str, tweet.retweet_count, tweet.favorite_count, tweet.entities["hashtags"],
                        tweet.lang, tweet.in_reply_to_status_id_str, tweet.in_reply_to_user_id_str, tweet.in_reply_to_screen_name, tweet.is_quote_status, tweet.user.screen_name, tweet.user.description, tweet.user.followers_count, tweet.user.verified, tweet.user.location] for tweet in tweets]

     # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list,columns=['Text', 'Created_at', 'Tweet_id', 'RT_count', 'Fav_count', 'Hashtags', 'Language',
                                                  'Reply_to_status_id', 'Reply_to_user_id', 'Reply_to_user', 'Quoted_status', 'Username', 'Bio_description', 'User_followers_count', 'Account_verified', 'User_location'])

    # Define username as filename without '@'
    filename = (re.findall(r'^@(.*)', username))
    # Save dataframe as username.csv
    tweets_df.to_csv(rf'output/{filename[0]}.csv', index = False)
    #Show how the file was saved
    print("File saved as: ", f'{filename[0]}.csv')

if __name__ == "__main__":
    main()
