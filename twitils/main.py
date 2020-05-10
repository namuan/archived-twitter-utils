from datetime import date

import click
from selenium import webdriver

from twitils.tools import start_session, stop_session
from twitils.tools.download_replies import grab_replies
from twitils.tools.parent_tweet import grab_parent
from twitils.tools.tweets_between import grab_tweets_between


@click.group()
def cli():
    click.echo("Twitter Utilities")


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--tweetid", help="Twitter Status Id", required=True)
def parent_tweet(account, tweetid):
    click.echo("Fetching parent of {} tweet in {} account".format(tweetid, account))
    start_session(webdriver.Firefox())
    grab_parent(account, tweetid)
    stop_session()


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--tweetid", help="Twitter Status Id", required=True)
def download_replies(account, tweetid):
    click.echo("Downloading replies of {} tweet in {} account".format(tweetid, account))
    start_session(webdriver.Firefox())
    grab_replies(account, tweetid)
    stop_session()


@cli.command()
@click.option("--account", help="Twitter Handle", required=True)
@click.option("--since", help="Search from this date. Format YYYY-MM-DD", required=True)
@click.option("--until", help="Search to this date. Format YYYY-MM-DD", required=True)
def tweets_between(account, since, until):
    click.echo("Downloading tweets of {} tweet from {} to {}".format(account, since, until))
    since = date.fromisoformat(since)
    until = date.fromisoformat(until)
    start_session(webdriver.Firefox())
    grab_tweets_between(account, since, until)
    stop_session()
