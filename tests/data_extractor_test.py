from pathlib import Path

from twitils.tools.navigation import extract_data_from


def test_data_extractor():
    # load html file
    sample_data = Path().cwd().joinpath("data", "sample_tweet.html").read_text()

    # run through extractor
    twitter_handler, status_id = extract_data_from(sample_data, "")

    # verify results
    assert twitter_handler == "jnptl"
    assert status_id == "1475958811894636545"
