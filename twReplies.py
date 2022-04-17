import configparser
import csv
import re
import tweepy as tw

def main():
    # Get API tokens
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    parser.sections()
    consumer_key = parser.get('twitter', 'consumer_key')
    consumer_secret = parser.get('twitter', 'consumer_secret')
    access_key = parser.get('twitter', 'access_key')
    access_secret = parser.get('twitter', 'access_secret')

    # Authentication with Twitter
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    # API
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Update these for the tweet you want to process replies to 'name' = the account username and you can find the tweet id within the tweet URL
    username = '@*****'
    tweet_id = '*****'

    # Query method for replies enlist str
    replies=[]
    for tweet in tw.Cursor(api.search,q='to:'+username, result_type='recent', timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)
    replies

    # Define username as filename without '@'
    filename = (re.findall(r'^@(.*)', username))

    # Saving tweets to 'csv' file
    with open(rf'output/{filename}.csv', 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('user', 'text', 'tweet id', 'date', 'in reply to status id'))
        csv_writer.writeheader()
        for tweet in replies:
            row = {'user': tweet.user.screen_name, 'text': tweet.text.replace('\n', ' '), 'tweet id': tweet.id, 'date': tweet.created_at, 'in reply to status id': tweet.in_reply_to_status_id}
            csv_writer.writerow(row)

if __name__ == "__main__":
    main()
