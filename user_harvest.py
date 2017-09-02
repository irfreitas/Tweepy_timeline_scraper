from __future__ import unicode_literals

import logging
import time
import tweepy
import json
import re
import os
from datetime import datetime

with open("twitter_handles.txt") as f:
    handles = f.read().splitlines()


logging.basicConfig(
    filename="user_harvest.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

consumer_key = "PUT KEY HERE"
consumer_secret = "PUT SECRET HERE"
access_token = "GET TOKEN FROM TWITTER HERE"
access_token_secret = "PUT TOKEN SECRET FROM TWITTER HERE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, retry_delay=60, retry_count=5)
api2 = tweepy.API(auth)


def tweet_handler(user_id, tweet):
    wj = tweet._json

    # to write to file
    with open("user_data/"+user_id+".json", "a+") as fw:
        json.dump(wj, fw)
        fw.write("\n")


def get_recent_id(user_id):
    if os.path.isfile("user_data/" + user_id + ".json"):
        with open("user_data/" + user_id + ".json") as f:
            all_tweets = f.readlines()
            most_recent_time = None
            most_recent_id = None
            for x in all_tweets:
                stripped = re.sub("\n$", '', x)
                tweet = json.loads(stripped)
                time = datetime.strptime(tweet['created_at'],  '%a %b %d %H:%M:%S +0000 %Y')
                id = tweet['id_str']
                if most_recent_time == None:
                    most_recent_time = time
                    most_recent_id = id
                else:
                    if time > most_recent_time:
                        most_recent_time = time
                        most_recent_id = id
                    else:
                        pass
            with open("user_data/"+user_id+"recentid.txt", "w") as ri:
                ri.write(most_recent_id)

            return most_recent_id


def harvest_user(user_id, since_id=None):
    # check existing files for most recent id using function
    if os.path.isfile("user_data/"+user_id+".json"):
        most_recent_id = get_recent_id(user_id)
        since_id = most_recent_id

    # get pages with cursor to iterate over user_timeslines, rate limiting
    pages = tweepy.Cursor(api.user_timeline,
                          since_id=since_id,
                          screen_name=user_id,
                          count=200,
                          wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True).pages()
    while True:
        try:
            # try:
            page = next(pages)
            time.sleep(4)
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
            page = next(pages)
        except StopIteration:
            break
        except tweepy.TweepError:
            time.sleep(30)
            page = next(pages)
        for tweet in page:
            tweet_handler(user_id, tweet)


def main():
    for user_name in handles:
        try:
            api2.get_user(screen_name=user_name)
            harvest_user(user_id=user_name)
            logging.info("done with " + user_name)
        except tweepy.TweepError:
            with open("failed_handles.txt", "a+") as fh:
                fh.write(user_name + "\n")


if __name__ == '__main__':
    main()
