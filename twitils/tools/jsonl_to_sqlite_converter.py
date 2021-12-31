from urllib import parse

import dataset


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


def clean_str(string):
    if isinstance(string, str):
        return string.replace("\n", " ").replace("\r", "")
    return None


def text(t):
    # need to look at original tweets for retweets for full text
    if t.get("retweeted_status"):
        t = t.get("retweeted_status")

    if "extended_tweet" in t:
        return t["extended_tweet"]["full_text"]
    elif "full_text" in t:
        return t["full_text"]
    else:
        return t["text"]


def coordinates(t):
    if "coordinates" in t and t["coordinates"]:
        return "%f %f" % tuple(t["coordinates"]["coordinates"])
    return None


def hashtags(t):
    return " ".join([h["text"] for h in t["entities"]["hashtags"]])


def media_photo(t):
    media_urls = []
    if "media" in t["entities"]:
        for media in t["entities"]["media"]:
            if media["type"] == "photo":
                media_urls.append(media["media_url_https"])

    return " ".join(media_urls)


def media_video(t):
    media_urls = []
    if "extended_entities" in t and "media" in t["extended_entities"]:
        for media in t["extended_entities"]["media"]:

            if media["type"] == "animated_gif":
                media_urls.append(media["media_url_https"])

            if "video_info" in media and media["video_info"]["variants"]:
                media_urls.append(media["video_info"]["variants"][-1]["url"])

    return " ".join(media_urls)


def urls(t):
    return " ".join([h["expanded_url"] or "" for h in t["entities"]["urls"]])


def place(t):
    if "place" in t and t["place"]:
        return t["place"]["full_name"]


def retweet_id(t):
    if "retweeted_status" in t and t["retweeted_status"]:
        return t["retweeted_status"]["id_str"]
    elif "quoted_status" in t and t["quoted_status"]:
        return t["quoted_status"]["id_str"]


def retweet_screen_name(t):
    if "retweeted_status" in t and t["retweeted_status"]:
        return t["retweeted_status"]["user"]["screen_name"]
    elif "quoted_status" in t and t["quoted_status"]:
        return t["quoted_status"]["user"]["screen_name"]


def retweet_user_id(t):
    if "retweeted_status" in t and t["retweeted_status"]:
        return t["retweeted_status"]["user"]["id_str"]
    elif "quoted_status" in t and t["quoted_status"]:
        return t["quoted_status"]["user"]["id_str"]


def favorite_count(t):
    if "retweeted_status" in t and t["retweeted_status"]:
        return t["retweeted_status"]["favorite_count"]
    else:
        return t["favorite_count"]


def tweet_url(t):
    return "https://twitter.com/%s/status/%s" % (t["user"]["screen_name"], t["id_str"])


def user_urls(t):
    u = t.get("user")
    if not u:
        return None
    urls = []
    if "entities" in u and "url" in u["entities"] and "urls" in u["entities"]["url"]:
        for url in u["entities"]["url"]["urls"]:
            if url["expanded_url"]:
                urls.append(url["expanded_url"])
    return " ".join(urls)


def tweet_type(t):
    # Determine the type of a tweet
    if t.get("in_reply_to_status_id"):
        return "reply"
    if "retweeted_status" in t:
        return "retweet"
    if "quoted_status" in t:
        return "quote"
    return "original"


import json
from dateutil.parser import parse as date_parse


def convert_to_dict(jl):
    t = json.loads(jl)
    get = t.get
    user = t.get("user").get
    return dict(
        status_id=get("id_str"),
        tweet_url=tweet_url(t),
        created_at=get("created_at"),
        parsed_created_at=date_parse(get("created_at")),
        user_screen_name=user("screen_name"),
        text=text(t),
        tweet_type=tweet_type(t),
        coordinates=coordinates(t),
        hashtags=hashtags(t),
        media_photo=media_photo(t),
        media_video=media_video(t),
        urls=urls(t),
        favorite_count=favorite_count(t),
        in_reply_to_screen_name=get("in_reply_to_screen_name"),
        in_reply_to_status_id=get("in_reply_to_status_id"),
        in_reply_to_user_id=get("in_reply_to_user_id"),
        lang=get("lang"),
        place=place(t),
        possibly_sensitive=get("possibly_sensitive"),
        retweet_count=get("retweet_count"),
        retweet_or_quote_id=retweet_id(t),
        retweet_or_quote_screen_name=retweet_screen_name(t),
        retweet_or_quote_user_id=retweet_user_id(t),
        source=get("source"),
        user_id=user("id_str"),
        user_created_at=user("created_at"),
        user_default_profile_image=user("default_profile_image"),
        user_description=user("description"),
        user_favourites_count=user("favourites_count"),
        user_followers_count=user("followers_count"),
        user_friends_count=user("friends_count"),
        user_listed_count=user("listed_count"),
        user_location=user("location"),
        user_name=user("name"),
        user_statuses_count=user("statuses_count"),
        user_time_zone=user("time_zone"),
        user_urls=user_urls(t),
        user_verified=user("verified"),
    )


def db_insert(table, jd):
    table.upsert(
        jd,
        ["status_id"],
    )


def convert_jsonl_sqlite(source_file, target_file):
    with open(source_file) as f:
        json_lines = [line.rstrip() for line in f]

    db_path = f"sqlite:///{target_file}"
    db = dataset.connect(db_path)
    table = db["tweet_data"]
    for jl in json_lines:
        jd = convert_to_dict(jl)
        db_insert(table, jd)
