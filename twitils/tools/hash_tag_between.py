from datetime import timedelta
from urllib import parse

from twitils.tools.navigation import scroll_to_last_page
from twitils.tools.writer import write_raw_tweets


def encode(src):
    return parse.quote_plus(src)


def since_query_param(since):
    return "since%3A{}".format(since)


def until_query_param(until):
    return "until%3A{}".format(until)


def search_query_builder(hash_tag, since, until):
    s = since_query_param(since)
    u = until_query_param(until)
    f = encode(hash_tag)
    return f"https://twitter.com/search?q=({f})%20{u}%20{s}&src=typed_query"


def date_range(since, until):
    for n in range(int((until - since).days)):
        yield since + timedelta(n)


def search_hash_tag_between(hash_tag: str, since, until):
    if not hash_tag.startswith("#"):
        hash_tag = "#{}".format(hash_tag)

    all_tweets = {}
    for d in date_range(since, until):
        full_url = search_query_builder(hash_tag, d, d + timedelta(1))
        print(f"🔎 Search URL: {full_url}")
        all_tweets = {**all_tweets, **scroll_to_last_page(full_url)}

    print(f"✅ Total tweets: {len(all_tweets)}")
    output_directory = write_raw_tweets(hash_tag, all_tweets)
    print("📝 Tweets written in {}".format(output_directory))
