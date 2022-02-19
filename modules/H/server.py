from flask import Flask
from flask import render_template
from flask import request

import validators
import concurrent.futures
import statistics

from . import news
from . import twitter
from . import sentiment
from . import utils

import time

app = Flask(__name__)


def get_article_with_score(url):
    article = news.get_article(url)
    score = sentiment.vader_sentiment(article.text)
    return (article, score)


def score_tweet(tweet):
    score = sentiment.vader_sentiment(tweet.text)
    return (tweet, score)


@app.route('/')
def index():
    return render_template('index.html',
            search_type='tweets')


@app.route('/search-news', methods=['POST'])
def search_news():
    print(request.form)
    query = request.form.get('query')
    from_date = request.form.get('start_date')
    to_date = request.form.get('end_date')

    articles = []
    sentiment_scores = {}

    if validators.url(query):
        article, score = get_article_with_score(query)
        articles = [article]
        sentiment_scores[article.url] = score
    else:
        article, score = get_article_with_score(query)
        articles_list = news.search_articles(
                query,
                100,
                from_date=from_date,
                to_date=to_date)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            for article_summary in articles_list:
                futures.append(executor.submit(get_article_with_score, article_summary['url']))

            for future in concurrent.futures.as_completed(futures):
                try:
                    article, score = future.result()
                    articles.append(article)
                    sentiment_scores[article.url] = score
                except e:
                    # TODO
                    print(e)

    search_id = utils.save_search_to_db(query, 'news', articles, sentiment_scores, from_date, to_date)
    for article in articles:
        utils.save_article_file(article, sentiment_scores[article.url])

    sentiment.run_biphone_scoring(search_id)

    mean_score = statistics.mean(sentiment_scores.values())
    median_score = statistics.median(sentiment_scores.values())
    std_dev = statistics.stdev(sentiment_scores.values()) if len(sentiment_scores) > 1 else None

    return render_template('index.html',
            search_type='news',
            articles=articles,
            form=request.form,
            sentiment_scores=sentiment_scores,
            mean_sentiment_score=mean_score,
            median_sentiment_score=median_score,
            std_dev_sentiment_scores=std_dev
            )


@app.route('/search-tweets', methods=['POST'])
def search_tweets():
    print(request.form)
    query = request.form.get('query')

    tweets = twitter.search_tweets(query, limit=250)
    sentiment_scores = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for tweet in tweets:
            futures.append(executor.submit(score_tweet, tweet))

        for future in concurrent.futures.as_completed(futures):
            try:
                tweet, score = future.result()
                sentiment_scores[tweet.id] = score
            except:
                # TODO
                pass

    mean_score = statistics.mean(sentiment_scores.values())
    median_score = statistics.median(sentiment_scores.values())
    std_dev = statistics.stdev(sentiment_scores.values()) if len(sentiment_scores) > 1 else None

    return render_template('index.html',
            search_type='tweets',
            tweets=tweets,
            form=request.form,
            sentiment_scores=sentiment_scores,
            mean_sentiment_score=mean_score,
            median_sentiment_score=median_score,
            std_dev_sentiment_scores=std_dev
            )


if __name__ == '__main__':
    app.run(debug=True)
