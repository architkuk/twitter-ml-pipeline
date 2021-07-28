from credentials import *
from twitter import Twitter, OAuth

t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))

orgs = ['Pfizer', 'Moderna', 'Johnson & Johnson']
for org in orgs:
    query = '#' + 'org'
    t.search.tweets(q=query)
