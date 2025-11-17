# QUERIES

# --------------------------Subreddit--------------------------
# QUERY TO INSERT BULK DATA INTO Subreddit TABLLE
BULK_INSERT_SUBREDDIT = "INSERT INTO Subreddit (unique_name, title, subscribers, description, lang, url, created_utc, icon_img, over18) VALUES %s"

# QUERY TO SELECT unique_name FROM Subreddit TABLLE
SELECT_UNIQUE_NAME_SUBREDDIT = "SELECT unique_name FROM Subreddit"

# --------------------------Posts--------------------------
BULK_INSERT_POSTS = "INSERT INTO posts (unique_name, author_fullname, author, title, subreddit, hidden, thumbnail, over_18, edited, created_at, id, is_video, post_details) VALUES %s ON CONFLICT (unique_name, created_timestamp) DO NOTHING"
SELECT_UNIQUE_NAME_POSTS = "SELECT unique_name FROM posts"

# --------------------------Comments--------------------------
BULK_INSERT_COMMENTS = "INSERT INTO comments (comment_id, subreddit_id, subreddit, author, parent_id, over_18, body, post_id, created_utc, link_id, comment_details) VALUES %s ON CONFLICT (comment_id, created_timestamp) DO NOTHING"
SELECT_UNIQUE_ID_COMMENTS = "SELECT comment_id FROM comments"

# --------------------------Toxicity--------------------------
INSERT_BULK_TOXICITY_DATA_QUERY = """
INSERT INTO toxicity (
  subreddit, titleOrComment, unique_name, comment, language,
  toxicity, severe_toxicity, identity_attack, insult, threat,
  profanity, sexually_explicit, flirtation, obscene, spam, unsubstantial
) VALUES %s
ON CONFLICT (subreddit, unique_name) DO UPDATE SET
  titleOrComment = EXCLUDED.titleOrComment,
  comment = EXCLUDED.comment,
  language = EXCLUDED.language,
  toxicity = EXCLUDED.toxicity,
  severe_toxicity = EXCLUDED.severe_toxicity,
  identity_attack = EXCLUDED.identity_attack,
  insult = EXCLUDED.insult,
  threat = EXCLUDED.threat,
  profanity = EXCLUDED.profanity,
  sexually_explicit = EXCLUDED.sexually_explicit,
  flirtation = EXCLUDED.flirtation,
  obscene = EXCLUDED.obscene,
  spam = EXCLUDED.spam,
  unsubstantial = EXCLUDED.unsubstantial,
  scored_at = now()
"""
