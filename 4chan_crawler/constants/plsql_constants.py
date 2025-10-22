# Queries

# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = "INSERT INTO boards (board_code, board_title, meta_description, ws_board) VALUES %s"

# Query to select all boards from the boards table
SELECT_BOARD_CODE_QUERY = "SELECT board_code FROM boards"

# Inserting data into threads table in PostgreSQL
INSERT_BULK_THREAD_DATA_QUERY = "INSERT INTO threads (thread_id, board_code, thread_title, com, created_time, last_modified, replies, semantic_url, images) VALUES %s"

# Query to select existing thread IDs for a specific board to avoid duplicates
SELECT_THREAD_IDS_QUERY = "SELECT thread_id FROM threads WHERE board_code = %s" 