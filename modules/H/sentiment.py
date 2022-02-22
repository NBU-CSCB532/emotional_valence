import os
import openpyxl

from main import main

from concurrent.futures import ThreadPoolExecutor
from ilock import ILock
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from . import utils

from .common import SEARCH_STATUS_COMPLETED
from .common import SEARCH_STATUS_ERROR

executor = ThreadPoolExecutor(1)


def vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']


def get_biphone_score_for_article(title):
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_workbook_path = os.path.join(script_path, '..', 'G', 'Final document weight and count.xlsx')
    input_workbook = openpyxl.load_workbook(input_workbook_path)
    input_sheet = input_workbook['Sheet1']
    for row in input_sheet.iter_rows(min_row=1):
        if row[0].value == title:
            return row[7].value


def get_biphone_score_for_twitter_search(filename):
    title = filename.replace('.docx', '')
    return get_biphone_score_for_article(title)


def news_biphone_scoring(search_id):
    with ILock('biphone_scoring_web'):
        try:
            print("Biphone scoring started!")

            main(no_cleaning=True)

            print("Biphone scoring completed! Will run post-scoring procedure now.")

            print('Updating documents in database')

            documents = utils.get_documents_for_search(search_id)
            for document in documents:
                doc_id = document[0];
                title = utils.slugify(document[1]);
                score = get_biphone_score_for_article(title)
                utils.update_document_biphone_score(doc_id, score)

            print('Updating the search status')
            utils.update_search_status(search_id, SEARCH_STATUS_COMPLETED)

            print('Done')
        except Exception as e:
            print(e)
            utils.update_search_status(search_id, SEARCH_STATUS_ERROR)


def run_news_biphone_scoring(search_id):
    executor.submit(news_biphone_scoring, search_id)


def twitter_biphone_scoring(search_id):
    with ILock('biphone_scoring_web'):
        try:
            print("Biphone scoring started!")

            main(no_cleaning=True)

            print("Biphone scoring completed! Will run post-scoring procedure now.")

            print('Updating twitter search results in database')

            search = utils.get_search(search_id)
            score = get_biphone_score_for_twitter_search(search[7])
            print('score is ', score)
            utils.update_search_biphone_score(search_id, score)

            print('Updating the search status')
            utils.update_search_status(search_id, SEARCH_STATUS_COMPLETED)

            print('Done')
        except Exception as e:
            print(e)
            utils.update_search_status(search_id, SEARCH_STATUS_ERROR)



def run_twitter_biphone_scoring(search_id):
    executor.submit(twitter_biphone_scoring, search_id)

