from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from flask import flash

import validators
import concurrent.futures
import scipy.stats
import statistics

from . import news
from . import twitter
from . import sentiment
from . import utils

import time
import os

TEMPLATE_KEYWORDS_FILE = 'KeyWords_template.xlsx'
KEYWORDS_FILE = 'KeyWords.xlsx'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
# WARNING: this env variable should be set to a truly secret value on production
app.secret_key = os.environ.get('SECRET_KEY', 'dev')


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
        article, score = news.get_article_with_score(query)
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
                futures.append(executor.submit(news.get_article_with_score, article_summary['url']))

            for future in concurrent.futures.as_completed(futures):
                try:
                    article, score = future.result()
                    articles.append(article)
                    sentiment_scores[article.url] = score
                except Exception as e:
                    # TODO
                    print(e)

    search_id = utils.save_news_search_to_db(query, articles, sentiment_scores, from_date, to_date)
    for article in articles:
        utils.save_article_file(article, sentiment_scores[article.url])

    sentiment.run_news_biphone_scoring(search_id)

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

    tweets = twitter.search_tweets(query, limit=100)
    sentiment_scores = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for tweet in tweets:
            futures.append(executor.submit(twitter.score_tweet, tweet))

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

    search_id = utils.save_twitter_search_to_db(query, tweets, sentiment_scores)
    utils.save_tweets_file(search_id, query, tweets, mean_score)

    sentiment.run_twitter_biphone_scoring(search_id)

    return render_template('index.html',
            search_type='tweets',
            tweets=tweets,
            form=request.form,
            sentiment_scores=sentiment_scores,
            mean_sentiment_score=round(mean_score, 2),
            median_sentiment_score=round(median_score, 2),
            std_dev_sentiment_scores=round(std_dev, 2)
            )


@app.route('/searches')
def searches():
    searches = utils.get_searches()
    return render_template('searches.html', searches=searches)


def show_news_search(search):
    search_id = search[0]
    documents = list(utils.get_documents_for_search(search_id))

    vader_scores = [d[6] for d in documents]
    biphone_scores = [d[7] for d in documents]

    correlation = scipy.stats.pearsonr(vader_scores, biphone_scores)[0]

    # remove None values
    vader_scores = [x for x in vader_scores if x]
    biphone_scores = [x for x in biphone_scores if x]

    vader_mean_score = statistics.mean(vader_scores)
    vader_median_score = statistics.median(vader_scores)
    vader_std_dev = statistics.stdev(vader_scores) if len(vader_scores) > 1 else None

    biphone_mean_score = statistics.mean(biphone_scores) if len(biphone_scores) > 1 else None
    biphone_median_score = statistics.median(biphone_scores) if len(biphone_scores) > 1 else None
    biphone_std_dev = statistics.stdev(biphone_scores) if len(biphone_scores) > 1 else None

    document_texts = {doc[1]: utils.read_document(doc[1], doc[6]) for doc in documents}

    return render_template('show_news_search.html',
            search=search,
            articles=documents,
            document_texts=document_texts,
            vader_mean_sentiment_score=vader_mean_score,
            vader_median_sentiment_score=vader_median_score,
            vader_std_dev_sentiment_scores=vader_std_dev,
            biphone_mean_sentiment_score=biphone_mean_score,
            biphone_median_sentiment_score=biphone_median_score,
            biphone_std_dev_sentiment_scores=biphone_std_dev,
            correlation=correlation)


def show_twitter_search(search):
    search_id = search[0]

    tweets = list(utils.get_tweets(search_id))

    vader_scores = [d[5] for d in tweets if d[5]]

    vader_mean_score = statistics.mean(vader_scores)
    vader_median_score = statistics.median(vader_scores)
    vader_std_dev = statistics.stdev(vader_scores) if len(vader_scores) > 1 else None

    # biphone score is aggregated score for all tweets in the search
    biphone_score = search[8]

    return render_template('show_twitter_search.html',
            search=search,
            tweets=tweets,
            vader_mean_sentiment_score=vader_mean_score,
            vader_median_sentiment_score=vader_median_score,
            vader_std_dev_sentiment_scores=vader_std_dev,
            biphone_score=biphone_score)


@app.route('/searches/<id>')
def show_search(id):
    search = utils.get_search(id)

    if search[2] == 'news':
        return show_news_search(search)
    else:
        return show_twitter_search(search)


@app.route('/template-keywords-file')
def get_template_keywords_file():
    directory = os.path.join(app.root_path, '..', '..', 'Texts as found input')
    return send_from_directory(directory, TEMPLATE_KEYWORDS_FILE, as_attachment=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-keywords-file', methods=['POST'])
def upload_keywords_file():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            directory = os.path.join(app.root_path, '..', '..', 'Texts as found input')
            file.save(os.path.join(directory, KEYWORDS_FILE))
            flash('Keywords file was updated!')
            return render_template('index.html', search_type='batch')


@app.route('/batch-search', methods=['POST'])
def batch_search():
    sentiment.run_batch_news_biphone_scoring()
    flash('Batch search started. This will take a while... You will find the results in the search history.')
    return render_template('index.html', search_type='batch')

if __name__ == '__main__':
    app.run(debug=True)
