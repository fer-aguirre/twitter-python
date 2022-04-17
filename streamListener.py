import configparser
import re
import time
import pandas as pd
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


# Get API tokens
parser = configparser.ConfigParser()
parser.read("config.ini")
parser.sections()
consumer_key = parser.get('twitter', 'consumer_key')
consumer_secret = parser.get('twitter', 'consumer_secret')
access_key = parser.get('twitter', 'access_key')
access_secret = parser.get('twitter', 'access_secret')

runtime = 15

#This is a basic listener that just prints text.
class MyStreamListener(StreamListener):

    def on_status(self, status):
        print(status.text, status.id_str)
        return True

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = MyStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    stream = Stream(auth, listener)

    # Define username
    username = 'username'

    #This line filter Twitter Streams to capture data by the keywords
    tweet_iter = stream.filter(track=[username])

    # Define username as filename without '@'
    filename = (re.findall(r'^@(.*)', username))

    time.sleep(runtime)
    stream.disconnect()

    tweets_list = []
    for tweet in tweet_iter:
        tweets_list.append(tweet.text, tweet.id_str)


    df = pd.DataFrame(tweets_list, columns=['Text', 'Id'])

    df.to_csv(f'./output/{filename}.csv', index=False)
