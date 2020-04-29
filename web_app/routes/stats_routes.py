from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from flask import Blueprint, jsonify, request, flash, redirect, render_template

from web_app.statsmodels import load_model, train_and_save_model
from web_app.models import User
from web_app.services.basilica_service import conn as basilica_connection

stats_routes = Blueprint('stats_routes', __name__)

# TODO accept some inputs related to the iris training data( x values)
@stats_routes.route('/stats/iris')
def iris():

    X, y = load_iris(return_X_y = True)
    clf = load_model() # make sure to pre-train the model first
    print('classifier:', clf)

    inputs = X[:2, :]

    print('Inputs:', inputs)

    clf.fit(X, y)
    result = clf.predict(inputs)
    print('PREDICTION:', result)
    return 'PREDICTION:' + str(result) # todo return as Json

@stats_routes.route('/stats/prediction', methods = ['POST'])
def twitoff_predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print(screen_name_a, screen_name_b, tweet_text)
    
    classifier = LogisticRegression(random_state = 42, solver = 'lbfgs', multi_class='multinomial')

    tweet_embeddings = []
    tweet_labels = []

    breakpoint()

    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    tweets_a = user_a.tweets
    tweets_b = user_b.tweets
    all_tweets = tweets_a + tweets_b

    for tweet in all_tweets:
        tweet_embeddings.append(tweet.embedding)
        tweet_labels.append(tweet.user.screen_name)

    print('Embeddings:', len(tweet_embeddings), 'Labels:', len(tweet_labels))

    classifier.fit(tweet_embeddings, tweet_labels)

    # make and return a prediction
    example_tweet_embedding = basilica_connection.embed_sentence(tweet_text, model = 'twitter')
    result = classifier.predict([example_tweet_embedding])
    
    print('RESULTS:', result[0])
    return render_template('prediction_results.html',
        screen_name_a = screen_name_a,
        screen_name_b = screen_name_b,
        tweet_text = tweet_text,
        screen_name_most_likely = result[0]
    )