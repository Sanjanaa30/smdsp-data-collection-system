# Queries

# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = "INSERT INTO boards (board_code, board_title, meta_description, ws_board) VALUES %s"

# Query to select all boards from the boards table
SELECT_BOARD_CODE_QUERY = "SELECT board_code FROM boards"

# Inserting data into threads table in PostgreSQL (updated for catalog.json data)
INSERT_BULK_THREAD_DATA_QUERY = """
INSERT INTO threads (
    thread_id, board_code, thread_title, comment_texts, poster_name, 
    created_time, last_modified, replies, images, semantic_url, 
    is_sticky, is_closed, country_code, has_media, bump_limit, image_limit
) VALUES %s
"""

# Query to select existing thread IDs for a specific board to avoid duplicates
SELECT_THREAD_IDS_QUERY = "SELECT thread_id FROM threads WHERE board_code = %s"

# Upsert query for catalog monitoring (insert new or update existing threads)
UPSERT_CATALOG_THREAD_DATA_QUERY = """
INSERT INTO threads (
    thread_id, board_code, thread_title, comment_texts, poster_name, 
    created_time, last_modified, replies, images, semantic_url, 
    is_sticky, is_closed, country_code, has_media, bump_limit, image_limit
) VALUES %s
ON CONFLICT (thread_id) 
DO UPDATE SET 
    last_modified = EXCLUDED.last_modified,
    replies = EXCLUDED.replies,
    images = EXCLUDED.images,
    is_sticky = EXCLUDED.is_sticky,
    is_closed = EXCLUDED.is_closed,
    last_seen_in_catalog = CURRENT_TIMESTAMP
""" 