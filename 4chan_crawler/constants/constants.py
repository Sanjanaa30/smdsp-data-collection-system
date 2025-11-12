CHAN_CRAWLER = "4chan_crawler"
COLD_START_CRAWLER = "cold_start_crawler"
LOG_FILE_NAME_COLD_START_CRAWLER = "cold_start_crawler.log"


# FAKTORY CONFIGURATIONS
FAKTORY_SERVER_URL = "FAKTORY_SERVER_URL"
FAKTORY_CONCURRENCY = "FAKTORY_CONCURRENCY"
FAKTORY_CONSUMER_ROLE = "consumer"
FAKTORY_PRODUCER_ROLE = "producer"

# Define which fields to extract from the API
POSTS_FIELDS = [
    "board_name",
    "no",
    "name",
    "sub",
    "com",
    "filename",
    "ext",
    "time",
    "resto",
    "country",
    "country_name",
    "replies",
    "images",
    "archived",
    "bumplimit",
    "archived_on",
]

# --- Toxicity scoring (Faktory + attrs) ---
TOX_QUEUE = "toxicity"
TOX_JOBTYPE = "score_post_toxicity"

# Perspective attributes we request
PERSPECTIVE_ATTRS = [
    "TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "THREAT"
]

# Env var name for default language (matches your .env)
DEFAULT_LANG_ENV = "PERSPECTIVE_LANG_DEFAULT"
DEFAULT_LANG = "en"