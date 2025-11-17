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

# --- Toxicity scoring (Faktory + attrs) ---
TOX_QUEUE = "toxicity-queue"
TOX_JOBTYPE = "toxicity_job"

# Perspective attributes we request
# Complete list of all available attributes from Google Perspective API
# Production attributes (supported in all languages):
PERSPECTIVE_ATTRS = [
    "TOXICITY",  # A rude, disrespectful, or unreasonable comment
    "SEVERE_TOXICITY",  # A very hateful, aggressive, disrespectful comment
    "IDENTITY_ATTACK",  # Negative or hateful comments targeting identity/demographic
    "INSULT",  # Insulting, inflammatory, or negative comment
    "PROFANITY",  # Swear words, curse words, or other obscene language
    "THREAT",  # Describes an intention to inflict pain, injury, or violence
    "SEXUALLY_EXPLICIT",  # Contains references to sexual acts, body parts, or other lewd content
    "FLIRTATION",  # Pickup lines, complimenting appearance, subtle sexual references
    "OBSCENE",  # Obscene or vulgar language
    "SPAM",  # Irrelevant or unsolicited message
    "UNSUBSTANTIAL",  # Trivial or short comments
]

# Env var name for default language (matches your .env)
DEFAULT_LANG_ENV = "PERSPECTIVE_LANG_DEFAULT"
DEFAULT_LANG = "en"
