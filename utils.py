from datetime import datetime, timedelta
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt


def search(headers, query, start_date, start_time, end_time, tweet_fields, max_results):
    try:
        url = ''
        if start_date == str(datetime.utcnow() - timedelta(days=7))[:10]:
            url = f'https://api.twitter.com/2/tweets/search/recent?query={query}%20lang:en&start_time={get_rfc3339_hr(start_date)}&end_time={end_time}&tweet.fields={tweet_fields}&max_results={max_results}'
        else:
            url = f'https://api.twitter.com/2/tweets/search/recent?query={query}%20lang:en&start_time={start_date}{start_time}&end_time={end_time}&tweet.fields={tweet_fields}&max_results={max_results}'
        return requests.get(url, headers=headers).json()
    except KeyError:
        print('KeyError')


def mean_sentiment(tweets):
    mean = 0
    for tweet in tweets:
        blob = TextBlob(tweet['text'])
        mean += 100*blob.sentiment.polarity
    return mean / len(tweets)


def create_plot(org, data, dates):
    plt.plot([str(date)[6:] for date in dates], data)
    plt.title(f'Sentiment Data for {org.title()} Between 7/26 and 8/1')
    plt.xlabel('Day')
    plt.ylabel('Average Sentiment')
    plt.savefig(f'./plots/{org}.png')
    plt.clf()


def increment_start_date(start_date):
    d = datetime.strptime(
        start_date, '%Y-%m-%d') + timedelta(days=1)
    return str(d)[:10]


def get_rfc3339_hr(start_date):
    d = datetime.utcnow()
    if d.hour < 23:
        return f'{start_date}T{d.hour + 1}:00:00Z'
    else:
        return f'{start_date}T00:00:00Z'


def now():
    return datetime.utcnow()
