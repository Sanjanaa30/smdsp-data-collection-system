# Queries
# Inserting data into boards table in PostgreSQL
INSERT_BULK_BOARD_DATA_QUERY = "INSERT INTO boards (board_code, board_title, meta_description, ws_board) VALUES %s"
# Query to select all boards from the boards table
SELECT_BOARD_CODE_QUERY = "SELECT board_code FROM boards"