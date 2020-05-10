from datetime import timedelta

from twitils.tools.navigation import (
    scroll_to_last_page,
)
from twitils.tools.writer import write_tweet_ids


def since_query_param(since):
    return "since%3A{}".format(since)


def until_query_param(until):
    return "until%3A{}".format(until)


def from_account_query_param(from_account):
    return "from%3A{}".format(from_account)


def search_query_builder(from_account, since, until):
    s = since_query_param(since)
    u = until_query_param(until)
    f = from_account_query_param(from_account)
    return f'https://twitter.com/search?q=({f})%20{u}%20{s}&src=typed_query'


def date_range(since, until):
    for n in range(int((until - since).days)):
        yield since + timedelta(n)


def grab_tweets_between(from_account, since, until):
    all_tweets = {}
    for d in date_range(since, until):
        full_url = search_query_builder(from_account, d, d + timedelta(1))
        print(f"🔎 Search URL: {full_url}")
        all_tweets = {**all_tweets, **scroll_to_last_page(full_url)}

    print(f"✅ Total tweets: {len(all_tweets)}")
    output_file_name = "{}_{}_{}.tweets.json".format(from_account, since, until)
    write_tweet_ids(output_file_name, all_tweets)
    print("📝 Tweets(identifiers) written in {}".format(output_file_name))
