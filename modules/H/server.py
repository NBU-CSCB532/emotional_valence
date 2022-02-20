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
        articles_list = news.search_articles(
                query,
                30,
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


@app.route('/searches')
def searches():
    searches = utils.get_searches()
    return render_template('searches.html', searches=searches)


@app.route('/searches/<id>')
def show_search(id):
    search = utils.get_search(id)
    documents = list(utils.get_documents_for_search(id))

    vader_scores = [d[6] for d in documents if d[6]]
    biphone_scores = [d[7] for d in documents if d[7]]

    vader_mean_score = statistics.mean(vader_scores)
    vader_median_score = statistics.median(vader_scores)
    vader_std_dev = statistics.stdev(vader_scores) if len(vader_scores) > 1 else None

    biphone_mean_score = statistics.mean(biphone_scores)
    biphone_median_score = statistics.median(biphone_scores)
    biphone_std_dev = statistics.stdev(biphone_scores) if len(biphone_scores) > 1 else None

    document_texts = {doc[1]: utils.read_document(doc[1], doc[6]) for doc in documents}

    if search[2] == 'news':
        return render_template('show_news_search.html',
                search=search,
                articles=documents,
                document_texts=document_texts,
                vader_mean_sentiment_score=vader_mean_score,
                vader_median_sentiment_score=vader_median_score,
                vader_std_dev_sentiment_scores=vader_std_dev,
                biphone_mean_sentiment_score=biphone_mean_score,
                biphone_median_sentiment_score=biphone_median_score,
                biphone_std_dev_sentiment_scores=biphone_std_dev)
    else:
        return render_template('show_tweets_search.html',
                search=search,
                documents=documents)


if __name__ == '__main__':
    app.run(debug=True)
