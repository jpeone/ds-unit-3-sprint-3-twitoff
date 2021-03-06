# web_app/routes/twitter_routes.py
from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import api as twitter_api
from web_app.services.basilica_service import conn as basilica_connection

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
    statuses = twitter_api.user_timeline(screen_name, tweet_mode = 'extended', count = 100, exclude_replies=True, include_rts=False)
    print('Statuses:', len(statuses))

    tweet_texts = [status.full_text for status in statuses]
    # fetch embedding for each tweet
    embeddings = list(basilica_connection.embed_sentences(tweet_texts, model="twitter")) 
    print('Embeddings:', len(embeddings))

    for index, status in enumerate(statuses):
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text

        embedding = embeddings[index]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        

    # store tweets in database( w/embeddings)
    db.session.commit()
    return jsonify({'user': user._json, 'num_tweets': len(statuses)})