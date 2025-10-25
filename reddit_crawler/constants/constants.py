# Logger
REDDIT_CRAWLER = "reddit_crawler"
COLD_START_CRAWLER = "cold_start_crawler"
LOG_FILE_NAME_COLD_START_CRAWLER = "cold_start_crawler.log"
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
    "is_video",
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
    "is_robot_indexable",
]


COMMENT_FIELDS = [
    "id",
    "subreddit_id",
    "subreddit",
    "author",
    "parent_id",
    "over_18",
    "body",
    "link_id",
    "created_utc",
    "link_url",
]

COMMENT_DETAILS_FIELDS = [
    "ups",
    "downs",
    "num_reports",
    "total_awards_received",
    "likes",
    "replies",
    "user_reports",
    "mod_reason_title",
    "gilded",
    "num_comments",
    "report_reasons",
    "removal_reason",
    "controversiality",
    "top_awarded_type",
]
