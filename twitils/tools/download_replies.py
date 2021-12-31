from twitils.tools import session
from twitils.tools.navigation import (
    scroll_to_top,
    get_first_tweet_on_page,
    url_builder,
    extract_data_from,
    scroll_to_last_page,
)
from twitils.tools.writer import write_raw_tweets


def find_parent_tweet(mentioned_tweet):
    session.current().get(mentioned_tweet)
    scroll_to_top()

    parent_tweet = get_first_tweet_on_page()
    tweet_html = parent_tweet.get_attribute("outerHTML")
    return extract_data_from(tweet_html, tweet_html)


def grab_replies(from_account, tweet_id):
    tweet_url = url_builder(from_account, tweet_id)
    print(f"✅ Tweet URL: {tweet_url}")
    all_tweets = scroll_to_last_page(tweet_url)
    print(f"✅ Total tweets: {len(all_tweets)}")
    output_directory = write_raw_tweets(f"replies-{from_account}-{tweet_id}", all_tweets)
    print("📝 Replies written in {}".format(output_directory))
