# sentiments
A playground for testing ideas for a sentiment analysis university project

# Install

You need Python 3 (seriously, who is still using Python 2?)

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

You also need to create a [Twitter developer account](https://developer.twitter.com) and a [Newsapi account](https://newsapi.org/).

Before starting the app you need to set the following environment variables:

```bash
export TWITTER_CONSUMER_KEY=<secret>
export TWITTER_BEARER_TOKEN=<secret>
export TWITTER_CONSUMER_SECRET=<secret>
export NEWS_API_KEY=<secret>
```

Then you can start the app:

```bash
python3 main.py
```
