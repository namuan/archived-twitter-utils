## twitter-utils

Note: Archived. See this https://github.com/namuan/twitter-utils

Collection of twitter utilities.

### Installation

Once generated, create output for twarc

nmn$ cat  | jq '.[] | @text' | tr -d '\"' > ~/workspace/twarc-work/ids.txt

```
$ pip install twitter-utils
```

### Usage

The following sub-commands are currently implemented

#### tweets_between

Download all tweet identifiers for an account between given dates.
Stores all tweet identifies in a file with the format "<twitter-handle>-<since-date>-<until-date>.tweets.json".

Sample run:
```
$ twitter-utils tweets-between --account DashCamTwats --since 2020-04-10 --until 2020-04-25
✅ Search URL: https://twitter.com/search?q=(from%3ADashCamTwats)%20until%3A2020-05-19%20since%3A2020-04-10&src=typed_query
... (progress)
✅ Total tweets: 114
📝 Tweets(identifiers) written in DashCamTwats_2020-04-10_2020-04-25.txt
```

#### parent_tweet

Find the parent tweet if you provide a reply of the original tweet. 
It prints the parent tweet URL along with Twitter handle and status identifier.

Sample run:
```
$ twitter-utils parent-tweet --account plastered41 --tweetid 1259071349152272386
✅ Replied Tweet URL: https://twitter.com/plastered41/status/1259071349152272386
👉 Parent Tweet URL: https://twitter.com/DashCamTwats/status/1259057703286116352
📝 Parent Tweet Handle: DashCamTwats, Status Id: 1259057703286116352
```  

#### download_replies

Find all the replies of a given tweet. 
Stores all tweet identifies in a file with the format "<twitter-handle>-<status-id>.tweets.json".

Sample run:
```
$ twitter-utils download-replies --account DashCamTwats --tweetid 1259057703286116352
✅ Tweet URL: https://twitter.com/DashCamTwats/status/1259057703286116352
... (progress)
🤩 Looks like we are done
✅ Total tweets: 41
📝 Replies(identifiers) written in DashCamTwats_1259057703286116352.txt
```

#### Get tweet ids from list of files in a directory

```shell
find backroom/raw-tweets/.../*.html | while read file; do basename $file ".html"; done > backroom/twarc-tweet-ids/....txt
```

#### Selecting WebDriver

`twitter-utils` uses Firefox by default, but it can be overridden by providing an alternate browser.
Supporting Firefox, Safari and Chrome.  

To use Safari instead of Firefox, pass the `--browser` option before specifying the sub-command.

```
twitter-utils --browser safari ...
```

And to use Chrome

```
twitter-utils --browser chrome ...
```

### Contributing

Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

You'll need a working version of `Python3` to run these scripts.

1) Create and use new virtual env

```
python3 -m venv venv
source venv/bin/activate
```

2) Install required dependencies

```
$ pip install -r requirements.txt
```

3) Run locally

```
$ python local_main.py ...
```

### Publishing Updates to PyPi

```shell
$ make package
```

Enter the username and password for pypi.org repo when prompted

### Similar Tools

[twarc](https://github.com/DocNow/twarc) A command line tool (and Python library) for archiving Twitter JSON

### License

[MIT](https://choosealicense.com/licenses/mit/)
