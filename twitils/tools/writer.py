import json
from pathlib import Path


def write_tweet_ids(output_file_name, tweets_element):
    tweet_ids = [twid for twid, _ in tweets_element.items() if twid is not "unknown"]
    tweet_ids_json = json.dumps(tweet_ids)
    Path(output_file_name).write_text(tweet_ids_json)
