# Tweepy_timeline_scraper
The project uses tweepy to scrape tweets from a user timeline and update the file if it already exists.  Assumes existence of a "user_data" subfolder within the current folder.  Requires you to add in your own Twitter credentials. Requires Python 3.

The Tweepy_timeline_scraper script will use the Twitter API to gather recent tweets from user timelines.  A list of twitter user names will be read from a file named "twitter_handles.txt" which has a user name on every new line.  The scripts checks for an existing line-delimited json file for each twitter user.  For a new user, a file is created and the recent tweets stored in it. For a user timeline that has previously been scraped, the script checks for the most recent id and gathers tweets which have been posted since then to append to the existing json file. 

To account for Twitter handles which have not been scraped correctly, a "failed_handles.txt" file will have the problematic user names written.  A "user_harvest.log" file receives all log output. 
