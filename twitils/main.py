import click
from selenium import webdriver

from twitils.tools import start_session, stop_session
from twitils.tools.parent_tweet import grab_parent


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
