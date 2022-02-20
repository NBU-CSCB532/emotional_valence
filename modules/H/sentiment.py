import os
import openpyxl

from main import main

from concurrent.futures import ThreadPoolExecutor
from ilock import ILock
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from . import utils

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


def biphone_scoring(search_id):
    with ILock('biphone_scoring_web'):
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
        utils.update_search_status(search_id, 'completed')

        print('Done')



def run_biphone_scoring(search_id):
    executor.submit(biphone_scoring, search_id)

