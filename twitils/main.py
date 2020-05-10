from datetime import date

import click

from twitils.tools import session
from twitils.tools.download_replies import grab_replies
from twitils.tools.parent_tweet import grab_parent
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
    click.echo("Downloading tweets of {} tweet from {} to {}".format(account, since, until))
    since = date.fromisoformat(since)
    until = date.fromisoformat(until)
    session.start()
    grab_tweets_between(account, since, until)
    session.stop()
