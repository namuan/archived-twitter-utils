import json
from pathlib import Path


def write_tweet_ids(output_file_name, tweets_element):
    tweet_ids = [twid for twid, _ in tweets_element.items() if twid != "unknown"]
    tweet_ids_json = json.dumps(tweet_ids)
    Path(output_file_name).write_text(tweet_ids_json)

def write_raw_tweets(tweets_group, tweets_element):
    output_directory = Path.cwd() / "backroom" / "raw-tweets" / tweets_group
    output_directory.mkdir(parents=True, exist_ok=True)

    for tweet_id, tweet_html in tweets_element.items():
        if tweet_id == "unknown":
            continue
        Path(output_directory).joinpath(tweet_id + ".html").write_text(tweet_html)

    return output_directory
