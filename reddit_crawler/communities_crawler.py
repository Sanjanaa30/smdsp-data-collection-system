from reddit_client import RedditClient
from constants import SUBREDDIT_URL

def get_communities():
    redditClient = RedditClient()
    print(redditClient.make_request(SUBREDDIT_URL))

get_communities()