import re

from time import sleep

from twitils.tools import get_session

delay = 5  # seconds


def url_builder(from_account, tweet_id):
    return f"https://twitter.com/{from_account}/status/{tweet_id}"


def get_first_tweet_on_page():
    selector = "//*[@role='article']"
    tweets_on_page = get_session().find_elements_by_xpath(selector)
    return tweets_on_page[0]


def scroll_to_top():
    sleep(delay)
    get_session().execute_script("window.scrollTo(0, 10);")


def extract_data_from(tweet):
    rgx = re.compile('a\stitle.*href="/(.*)/status/(\d+)"')
    matches = rgx.findall(tweet)

    twitter_handle = "unknown"
    status_id = "unknown"

    if not matches:
        print("Unable to find twitter status identifier in \n {}".format(tweet))
    else:
        twitter_handle, status_id = matches[0]

    return twitter_handle, status_id
