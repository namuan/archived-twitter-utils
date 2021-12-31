from datetime import date

import click

from twitils.tools import session
from twitils.tools.download_replies import grab_replies
from twitils.tools.hash_tag_between import search_hash_tag_between
from twitils.tools.jsonl_to_sqlite_converter import convert_jsonl_sqlite
from twitils.tools.parent_tweet import grab_parent
from twitils.tools.report_generator import generate_report
from twitils.tools.tweets_between import grab_tweets_between


@click.group()
@click.option("--browser", help="Selenium Browser", default="firefox")
def cli(browser):
    click.echo("Twitter Utilities: Using Browser {}".format(browser))
    session.update_browser(browser)


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--tweetid", help="Twitter Status Id", required=True)
def parent_tweet(account, tweetid):
    click.echo("Fetching parent of {} tweet in {} account".format(tweetid, account))
    session.start()
    grab_parent(account, tweetid)
    session.stop()


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--tweetid", help="Twitter Status Id", required=True)
def download_replies(account, tweetid):
    click.echo("Downloading replies of {} tweet in {} account".format(tweetid, account))
    session.start()
    grab_replies(account, tweetid)
    session.stop()


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--since", help="Search from this date. Format YYYY-MM-DD", required=True)
@click.option("--until", help="Search to this date. Format YYYY-MM-DD", required=True)
def tweets_between(account, since, until):
    click.echo(
        "Downloading tweets of {} tweet from {} to {}".format(account, since, until)
    )
    since = date.fromisoformat(since)
    until = date.fromisoformat(until)
    session.start()
    grab_tweets_between(account, since, until)
    session.stop()


@cli.command()
@click.option("--hash-tag", help="Hash Tag", required=True)
@click.option("--since", help="Search from this date. Format YYYY-MM-DD", required=True)
@click.option("--until", help="Search to this date. Format YYYY-MM-DD", required=True)
def hash_tag_search(hash_tag, since, until):
    click.echo(
        "Downloading tweets of hash tag {} from {} to {}".format(hash_tag, since, until)
    )
    since = date.fromisoformat(since)
    until = date.fromisoformat(until)
    session.start()
    search_hash_tag_between(hash_tag, since, until)
    session.stop()


@cli.command()
@click.option("--source-file", help="Full path of the JSONLines file", required=True)
@click.option("--target-file", help="Sqlite3 output file", required=True)
def jsonl_sqlite(source_file, target_file):
    click.echo("Converting {} and writing to {}".format(source_file, target_file))
    convert_jsonl_sqlite(source_file, target_file)


@cli.command()
@click.option("--source-file", help="Full path of the Ids file", required=True)
@click.option("--target-file", help="Target JSONLines file", required=True)
def twarc_downloader(source_file, target_file):
    click.echo(
        "Downloads Ids from {} and writing to {}".format(source_file, target_file)
    )


@cli.command()
@click.option("--source-file", help="Path to Sqlite3 database file", required=True)
def report_generator(source_file):
    click.echo("Generating report from {}".format(source_file))
    generate_report(source_file)
