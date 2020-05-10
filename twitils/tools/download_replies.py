from twitils.tools import session
from twitils.tools.navigation import (
    scroll_to_top,
    get_first_tweet_on_page,
    url_builder,
    extract_data_from,
    scroll_to_last_page,
)
from twitils.tools.writer import write_tweet_ids


def find_parent_tweet(mentioned_tweet):
    session.current().get(mentioned_tweet)
    scroll_to_top()

    parent_tweet = get_first_tweet_on_page()
    tweet_html = parent_tweet.get_attribute("outerHTML")
    return extract_data_from(tweet_html)


def grab_replies(from_account, tweet_id):
    tweet_url = url_builder(from_account, tweet_id)
    print(f"✅ Tweet URL: {tweet_url}")
    tweets_element = scroll_to_last_page(tweet_url)
    print(f"✅ Total tweets: {len(tweets_element)}")
    output_file_name = "{}_{}.tweets.json".format(from_account, tweet_id)
    write_tweet_ids(output_file_name, tweets_element)
    print("📝 Replies(identifiers) written in {}".format(output_file_name))
