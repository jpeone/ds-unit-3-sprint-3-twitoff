import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
print(type(auth)) #> <class 'tweepy.auth.OAuthHandler'>

api = tweepy.API(auth)
print(type(api)) #> <class 'tweepy.api.API'>

if __name__ == '__main__':

    print("-----------------")
    print("USER")
    user = api.get_user("elonmusk")
    print(type(user)) #> <class 'tweepy.models.User'>
    print(user.screen_name)
    print(user.id)
    print(user.statuses_count)
    
    print("-----------------")
    print("STATUSES")
    #statuses = api.user_timeline("elonmusk", count=35)
    #for status in statuses:
    #    print("--")
    #    print(status.text)
    
    statuses = api.user_timeline("elonmusk", tweet_mode="extended", count=35, exclude_replies=True, include_rts=False)
    for status in statuses:
        print("--")
        print(status.full_text)
    
    status = statuses[0]
    print(type(status)) #> <class 'tweepy.models.Status'>
    
    print(status.id)
    print(status.full_text)