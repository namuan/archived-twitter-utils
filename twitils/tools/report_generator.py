import dataset
import mistune


def md_to_html(src):
    return mistune.markdown(src)


def print_tweet(tweet_row):
    (
        id,
        status_id,
        tweet_url,
        created_at,
        parsed_created_at,
        user_screen_name,
        text,
        tweet_type,
        coordinates,
        hashtags,
        media_photo,
        media_video,
        urls,
        favorite_count,
        in_reply_to_screen_name,
        in_reply_to_status_id,
        in_reply_to_user_id,
        lang,
        place,
        possibly_sensitive,
        retweet_count,
        retweet_or_quote_id,
        retweet_or_quote_screen_name,
        retweet_or_quote_user_id,
        source,
        user_id,
        user_created_at,
        user_default_profile_image,
        user_description,
        user_favourites_count,
        user_followers_count,
        user_friends_count,
        user_listed_count,
        user_location,
        user_name,
        user_statuses_count,
        user_time_zone,
        user_urls,
        user_verified,
    ) = tweet_row.values()

    md = []
    for _ in range(0, 1):
        md.append("")
        md.append("---")

    md.append("")
    md.append("**Date** {0}".format(created_at))
    md.append("")
    md.append("**Tweet by** {0}".format(user_name))
    md.append("")
    md.append("[{0}]({0})".format(tweet_url))
    md.append("")
    md.append("**Tweet:**")
    md.append("```")
    md.append(text)
    md.append("```")

    photo_links = media_photo.split(" ") if media_photo else []
    for link in photo_links:
        md.append("")
        md.append("![{0}]({0})".format(link))

    video_links = media_video.split(" ") if media_video else []

    for link in video_links:
        md.append("[Video]({})".format(link))

    md.append("")
    md.append("**Retweets** {0} | **Likes** {1}".format(retweet_count, favorite_count))

    return md_to_html("\n".join(md))


def generate_report(source_file):
    db_path = f"sqlite:///{source_file}"
    db = dataset.connect(db_path)
    table = db["tweet_data"]
    html_fragments = []
    for tweet_row in table.find():
        html_fragments.append(print_tweet(tweet_row))

    print("<br/>".join(html_fragments))
