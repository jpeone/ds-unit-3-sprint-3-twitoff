# web_app/routes/twitter_routes.py
from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import api as twitter_api

from flask import Blueprint, jsonify#, request, render_template, flash, redirect

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name):
    print('Fetching...', screen_name)

    # fetch user info
    user = twitter_api.get_user(screen_name)

    # store user in database
    db_user = User.query.get(user.id) or User(id=user.id)
    db_user.screen_name = user.screen_name
    db_user.name = user.name
    db_user.location = user.location
    db_user.followers_count = user.followers_count
    db.session.add(db_user)

    # fetch their tweets
    statuses = twitter_api.user_timeline(screen_name, tweet_mode = 'extended', count = 35, exclude_replies=True, include_rts=False)

    # fetch embedding for each tweet

    for status in statuses:
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        #embedding = embeddings[counter]
        #print(len(embedding))
        #db_tweet.embedding = embedding
        db.session.add(db_tweet)
        #counter+=1
        

    # store tweets in database( w/embeddings)
    db.session.commit()
    return jsonify({'user': user._json, 'num_tweets': len(statuses)})