from twitils.tools.hash_tag_between import search_query_builder


def test_search_query_builder():
    hash_tag = "#BlahBlahBlah"
    until = "2020-03-15"
    since = "2020-03-01"

    output = search_query_builder(hash_tag, since, until)

    assert output == "https://twitter.com/search?q=(%23BlahBlahBlah)%20until%3A2020-03-15%20since%3A2020-03-01&src=typed_query"
