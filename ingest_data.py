import pandas as pd

from credentials import bearer_token
from utils import search, mean_sentiment, create_plot

# twitter search url example:
# 'https://api.twitter.com/2/tweets/search/recent?query=pfizer%20lang:en&end_time=2021-07-29T00:00:00.000Z&tweet.fields=created_at,in_reply_to_user_id'


def ingest_data():
    headers = {"Authorization": f"Bearer {bearer_token}"}

    start_time, end_time = 'T00:00:00Z', 'T23:59:59Z'
    dates = [f'2021-07-{dd}' for dd in range(26, 32)] + ['2021-08-01']
    orgs = open('input.txt', 'r')

    csv_data = []
    for org in orgs:
        org = org.rstrip()
        print(f'ORGANIZATION NAME: {org.upper()}')
        avg = 0
        data = []
        for date in dates:
            res = search(headers, org, date,
                         start_time, f'{date}{end_time}', 'public_metrics', 100)
            try:
                data.append(mean_sentiment(res['data']))
                for tweet in res['data']:
                    csv_data.append([org, date, tweet['text'], tweet['public_metrics']['like_count'],
                                     tweet['public_metrics']['reply_count'], tweet['public_metrics']['retweet_count'],
                                     tweet['public_metrics']['quote_count']])
            except KeyError:
                print('KeyError')
        create_plot(org, data, dates)

    df = pd.DataFrame(csv_data)
    df.to_csv('./data/tweet_data.csv')
