# Logger
REDDIT_CRAWLER = "reddit_crawler"
COLD_START_CRAWLER="cold_start_crawler"
LOG_FILE_NAME_COLD_START_CRAWLER="cold_start_crawler.log"
# FAKTORY CONFIGURATIONS
FAKTORY_SERVER_URL = "FAKTORY_SERVER_URL"
FAKTORY_CONSUMER_ROLE = "consumer"
FAKTORY_PRODUCER_ROLE = "producer"

# ITEMS TO BE COLLECTED
SUBREDDIT_FIELDS = [
    "name",
    "title",
    "subscribers",
    "description",
    "lang",
    "url",
    "created_utc",
    "icon_img",
    "over18",
]

POST_FIELDS = [
    "name",
    "author_fullname",
    "author",
    "title",
    "subreddit",
    "hidden",
    "thumbnail",
    "over_18",
    "edited",
    "created",
    "id",
    "is_video"
]

POST_DETAILED_FIELDS = [
    "is_original_content",
    "pwls",
    "num_comments",
    "top_awarded_type",
    "downs",
    "upvote_ratio",
    "hide_score",
    "ups",
    "quarantine",
    "total_awards_received",
    "num_reports",
    "gilded",
    "url_overridden_by_dest",
    "removal_reason",
    "is_robot_indexable"
]
