# QUERIES

# --------------------------Communities--------------------------
# QUERY TO INSERT BULK DATA INTO COMMUNITIES TABLLE
BULK_INSERT_COMMUNITIES = "INSERT INTO communities (unique_name, title, subscribers, description, lang, url, created_utc, icon_img, over18) VALUES %s"

# QUERY TO SELECT unique_name FROM COMMUNITIES TABLLE
SELECT_UNIQUE_NAME_COMMUNITY = "SELECT unique_name FROM communities"

# --------------------------Posts--------------------------
BULK_INSERT_POSTS = "INSERT INTO posts (unique_name, author_fullname, author, title, subreddit, hidden, thumbnail, over_18, edited, created_at, id, is_video, post_details) VALUES %s"
SELECT_UNIQUE_NAME_POSTS = "SELECT unique_name FROM posts"

