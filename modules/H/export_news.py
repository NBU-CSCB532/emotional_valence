import csv
import sys

import news
import sentiment

if __name__ == '__main__':
    with open(sys.argv[1], mode='r') as file:
      reader = csv.reader(file)

      for line in reader:
          url = line[0]
          article = news.get_article(url)
          score = sentiment.vader_sentiment(article.text)
          print('{},{}'.format(url, score))

