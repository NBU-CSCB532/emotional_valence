# import subprocess

from main import main

from concurrent.futures import ThreadPoolExecutor
from ilock import ILock
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


executor = ThreadPoolExecutor(1)


def vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']


def biphone_scoring(search_id):
    with ILock('biphone_scoring_web'):
        print("Biphone scoring started!")
        main(no_cleaning=True)
        print("Biphone scoring completed!")
        # subprocess.run(['python', 'main.py'])


def run_biphone_scoring(search_id):
    executor.submit(biphone_scoring, search_id)

