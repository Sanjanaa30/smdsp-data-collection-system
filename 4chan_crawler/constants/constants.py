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
TOX_QUEUE = "toxicity-queue"
TOX_JOBTYPE = "toxicity_job"

# Perspective attributes we request
# Complete list of all available attributes from Google Perspective API
# Production attributes (supported in all languages):
PERSPECTIVE_ATTRS = [
    "TOXICITY",              # A rude, disrespectful, or unreasonable comment
    "SEVERE_TOXICITY",       # A very hateful, aggressive, disrespectful comment
    "IDENTITY_ATTACK",       # Negative or hateful comments targeting identity/demographic
    "INSULT",                # Insulting, inflammatory, or negative comment
    "PROFANITY",             # Swear words, curse words, or other obscene language
    "THREAT",                # Describes an intention to inflict pain, injury, or violence
    "SEXUALLY_EXPLICIT",     # Contains references to sexual acts, body parts, or other lewd content
    "FLIRTATION",            # Pickup lines, complimenting appearance, subtle sexual references
    "OBSCENE",               # Obscene or vulgar language
    "SPAM",                  # Irrelevant or unsolicited message
    "UNSUBSTANTIAL",         # Trivial or short comments
]

# Env var name for default language (matches your .env)
DEFAULT_LANG_ENV = "PERSPECTIVE_LANG_DEFAULT"
DEFAULT_LANG = "en"