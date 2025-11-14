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

# Query to check which post numbers DO NOT exist in the database for a given board
# Returns only the post numbers that are not present in the database
CHECK_EXISTING_POSTS_QUERY = """
SELECT candidate_post_no
FROM unnest(%s::bigint[]) AS candidate_post_no
WHERE NOT EXISTS (
    SELECT 1 FROM posts 
    WHERE board_name = %s AND post_no = candidate_post_no
);
"""