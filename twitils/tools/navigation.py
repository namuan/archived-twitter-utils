import re

from time import sleep

from twitils.tools import session

DELAY = 5  # seconds
SELECTOR = "//*[@role='article']"


def url_builder(from_account, tweet_id):
    return f"https://twitter.com/{from_account}/status/{tweet_id}"


def get_first_tweet_on_page():
    tweets_on_page = session.current().find_elements_by_xpath(SELECTOR)
    return tweets_on_page[0]


def scroll_to_top():
    sleep(DELAY)
    session.current().execute_script("window.scrollTo(0, 10);")


def get_tweets_on_page():
    tweets_on_page = session.current().find_elements_by_xpath(SELECTOR)
    no_of_tweets_on_page = len(tweets_on_page)
    print("🔄 Total number of tweets on screen: {}".format(no_of_tweets_on_page))
    return tweets_on_page, no_of_tweets_on_page


def scroll_to_end():
    sleep(DELAY)  # sleep before scrolling
    session.current().execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(DELAY)  # For the page to catch up before we count again
    print("⬇️ Scroll down")


def scroll_to_last_page(full_url):
    session.current().get(full_url)
    sleep(DELAY)

    tweets_with_html = {}

    tweets_not_changed_on_screen_counter = 0
    max_count_if_tweets_dont_change = 4
    last_count_tweets_on_page = 0

    try:
        tweets_on_page, no_of_tweets_on_page = get_tweets_on_page()

        while tweets_not_changed_on_screen_counter < max_count_if_tweets_dont_change:
            if no_of_tweets_on_page == last_count_tweets_on_page:
                tweets_not_changed_on_screen_counter += 1
                print("🤔 Tweets not changed since last {} attempts - Last count: {}".format(
                    tweets_not_changed_on_screen_counter, last_count_tweets_on_page
                ))
            else:
                tweets_not_changed_on_screen_counter = 0

            last_count_tweets_on_page = no_of_tweets_on_page

            for tweet in tweets_on_page:
                tweet_html = tweet.get_attribute('outerHTML')
                _, status_id = extract_data_from(tweet_html, tweet.text)
                tweets_with_html[status_id] = tweet_html

            scroll_to_end()
            tweets_on_page, no_of_tweets_on_page = get_tweets_on_page()
        else:
            print("🤩 Looks like we are done")

    except Exception as e:
        print("❌ Exception raised during collecting tweets: {}".format(e))

    return tweets_with_html


def extract_data_from(tweet, tweet_text):
    rgx = re.compile('a\stitle.*href=\"/(.*)/status/(\d+)\"')
    matches = rgx.findall(tweet)

    twitter_handle = "unknown"
    status_id = "unknown"

    if not matches:
        print("❌ Unable to find twitter status identifier in \n => {}".format(tweet_text))
    else:
        twitter_handle, status_id = matches[0]

    return twitter_handle, status_id

