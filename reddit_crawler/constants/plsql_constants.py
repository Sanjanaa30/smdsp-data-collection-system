# QUERIES

# QUERY TO INSERT BULK DATA INTO COMMUNITIES TABLLE
BULK_INSERT_COMMUNITIES = "INSERT INTO communities (unique_name, title, subscribers, description, lang, url, created_utc, icon_img, over18) VALUES %s"

# QUERY TO SELECT unique_name FROM COMMUNITIES TABLLE
SELECT_unique_name_QUERY = "SELECT unique_name FROM communities"