# Queries

# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = (
    "INSERT INTO boards (board_code, board_title, meta_description, ws_board) VALUES %s"
)

# Query to select all boards from the boards table
SELECT_BOARD_CODE_QUERY = "SELECT board_code FROM boards"

# Query to insert posts into posts table
INSERT_BULK_POSTS_DATA_QUERY = "INSERT INTO posts (board_name, post_no, name, subject, comment, filename, ext, post_time, resto, country, country_name, replies, images, archived, bumplimit, archived_on) VALUES %s ON CONFLICT (board_name, post_no, created_at) DO NOTHING;"

SELECT_COUNT_BOARD_QUERY = "SELECT board_name, date_trunc('hour', created_at) AS hour, COUNT(*) AS post_count FROM posts GROUP BY board_name, hour ORDER BY hour DESC;"
SELECT_COUNT_HOUR_QUERY = "SELECT date_trunc('hour', created_at) AS hour, COUNT(*) AS post_count FROM posts GROUP BY hour ORDER BY hour DESC;"

# Select the latest row of a post (by board & post_no) in order to get its comment text
# Gives one row per (board_name, post_no) pair” (the first one according to the ORDER BY below).
SELECT_LATEST_POST_TEXT = """
SELECT DISTINCT ON (board_name, post_no)
       board_name, post_no, comment
FROM posts
WHERE board_name = %s AND post_no = %s
ORDER BY board_name, post_no, created_at DESC;
"""

# insert or update a row in post_toxicity so there is just one row per post.
# “Overwrite the existing row’s columns with the new ones from the INSERT.”
UPSERT_POST_TOXICITY = """
INSERT INTO post_toxicity (
  board_name, post_no, language,
  toxicity, severe_toxicity, identity_attack, insult, threat, scored_at
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, now())
ON CONFLICT (board_name, post_no) DO UPDATE SET
  language = EXCLUDED.language, 
  toxicity = EXCLUDED.toxicity,
  severe_toxicity = EXCLUDED.severe_toxicity,
  identity_attack = EXCLUDED.identity_attack,
  insult = EXCLUDED.insult,
  threat = EXCLUDED.threat,
  scored_at = now();
"""

# Find posts that don't have a toxicity row yet (for backfill)
# Because when you first add toxicity scoring, you already have lots of old posts in the posts table that were never scored.
#A LEFT JOIN is a type of SQL join that says:
# “Give me all rows from the left table, and if there’s matching data in the right table, include it — otherwise, fill it with NULL.”
# Why Left Join here? it lets us keep every post and then easily check which ones are missing toxicity.
SELECT_UNSCORED_POSTS = """
WITH latest AS (
  SELECT DISTINCT ON (board_name, post_no)
         board_name, post_no
  FROM posts
  ORDER BY board_name, post_no, created_at DESC
)
SELECT l.board_name, l.post_no
FROM latest l
LEFT JOIN post_toxicity s
  ON s.board_name = l.board_name AND s.post_no = l.post_no
WHERE s.post_no IS NULL
LIMIT %s;
"""
