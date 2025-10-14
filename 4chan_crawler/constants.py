FOURCHAN_BASE_URL = "https://a.4cdn.org"
FAKTORY_BASE_URL = "localhost:7420"
FAKTORY_PASSWORD = "password"

# Queries
# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = "INSERT INTO boards (board_code, board_title) VALUES %s"
# Query to select all boards from the boards table
SELECT_ALL_BOARDS_QUERY = "SELECT * FROM boards"