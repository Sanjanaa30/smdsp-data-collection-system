# Queries

# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = "INSERT INTO boards (board_code, board_title, meta_description, ws_board) VALUES %s"

# Query to select all boards from the boards table
SELECT_BOARD_CODE_QUERY = "SELECT board_code FROM boards"

# Query to insert posts into posts table
INSERT_BULK_POSTS_DATA_QUERY = "INSERT INTO posts (board_name, post_no, name, subject, comment, filename, ext, post_time, resto, country, country_name, replies, images, archived, bumplimit, archived_on) VALUES %s ON CONFLICT (post_no) DO NOTHING;"
