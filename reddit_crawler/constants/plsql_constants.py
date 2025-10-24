# QUERIES

# --------------------------Subreddit--------------------------
# QUERY TO INSERT BULK DATA INTO Subreddit TABLLE
BULK_INSERT_SUBREDDIT = "INSERT INTO Subreddit (unique_name, title, subscribers, description, lang, url, created_utc, icon_img, over18) VALUES %s"

# QUERY TO SELECT unique_name FROM Subreddit TABLLE
SELECT_UNIQUE_NAME_SUBREDDIT = "SELECT unique_name FROM Subreddit"

# --------------------------Posts--------------------------
BULK_INSERT_POSTS = "INSERT INTO posts (unique_name, author_fullname, author, title, subreddit, hidden, thumbnail, over_18, edited, created_at, id, is_video, post_details) VALUES %s ON CONFLICT (unique_name, created_timestamp) DO NOTHING"
SELECT_UNIQUE_NAME_POSTS = "SELECT unique_name FROM posts"
