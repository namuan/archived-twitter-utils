import click

from twitils.tools import session
from twitils.tools.navigation import (
    scroll_to_top,
    get_first_tweet_on_page,
    url_builder,
    extract_data_from,
)


def find_parent_tweet(mentioned_tweet):
    session.current().get(mentioned_tweet)
    scroll_to_top()

    parent_tweet = get_first_tweet_on_page()
    tweet_html = parent_tweet.get_attribute("outerHTML")
    return extract_data_from(tweet_html, parent_tweet.text)


def grab_parent(from_account, tweet_id):
    tweet_reply = url_builder(from_account, tweet_id)
    click.echo(f"✅ Replied Tweet URL: {tweet_reply}")
    parent_tweet_handle, parent_tweet_id = find_parent_tweet(tweet_reply)
    parent_tweet_url = url_builder(parent_tweet_handle, parent_tweet_id)
    click.echo(f"👉 Parent Tweet URL: {parent_tweet_url}")
    click.echo(
        f"📝 Parent Tweet Handle: {parent_tweet_handle}, Status Id: {parent_tweet_id}"
    )
