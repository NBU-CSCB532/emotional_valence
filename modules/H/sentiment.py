from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']
