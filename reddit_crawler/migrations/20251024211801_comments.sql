-- Table: Comments
-- Stores comments from Reddit, including detailed statistics.

CREATE TABLE comments (
    comment_id TEXT NOT NULL,                      -- Unique identifier for the comment like "nl77ej4"
    subreddit_id TEXT,                             -- Unique identifier for the subreddit
    subreddit TEXT,                                -- Subreddit where the comment was made
    author TEXT,                                   -- Reddit username of the author
    parent_id TEXT,                                -- Parent comment ID if the comment is a reply
    over_18 BOOLEAN,                               -- NSFW flag
    body TEXT,                                     -- The actual content of the comment
    post_id TEXT,                                  -- Foreign key to the related post ID (post_no)
    created_utc BIGINT,                            -- UNIX timestamp (in seconds)
    link_id TEXT NOT NULL,                         -- URL of the linked content (usually the post)
    comment_details JSONB NOT NULL,                -- Embedded JSONB with additional comment metadata
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the comment was created
);

-- The link_id column references posts(unique_name)s
-- Create hypertable partitioned by created_timestamp (time-based partitioning)
SELECT create_hypertable(
    'comments',
    'created_timestamp',
    chunk_time_interval => INTERVAL '1 day'
);

-- Create unique index for comments to ensure no duplicate comment entries
CREATE UNIQUE INDEX IF NOT EXISTS comments_unique_idx ON comments (comment_id, created_timestamp);

-- Create index on link_id for faster lookups when joining with posts
CREATE INDEX IF NOT EXISTS comments_link_id_idx ON comments (link_id);