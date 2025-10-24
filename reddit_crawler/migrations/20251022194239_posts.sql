-- Table: Posts
-- Stores post from the Reddit.

CREATE TABLE posts (
    unique_name TEXT NOT NULL,                     -- Unique identifier like "t3_abcd1234"
    author_fullname TEXT,                          -- Full name of the Reddit user
    author TEXT,                                   -- Reddit username
    title TEXT,                                    -- Title of the post
    subreddit TEXT,                                -- Subreddit where the post was made
    hidden BOOLEAN,                                -- Whether the post is hidden by the user
    thumbnail TEXT,                                -- URL to the thumbnail image
    over_18 BOOLEAN,                               -- NSFW flag
    edited BOOLEAN,                                -- Whether the post has been edited
    created_at BIGINT,                             -- UNIX timestamp (in seconds)
    id TEXT,                                       -- Post ID (optional if unique_name is unique enough)
    is_video BOOLEAN,                              -- Whether the post is a video
    post_details JSONB NOT NULL,                   -- Embedded JSONB with additional post metadata
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create hypertable partitioned by created_timestamp (time-based partitioning)
SELECT create_hypertable(
    'posts',
    'created_timestamp',
    chunk_time_interval => INTERVAL '1 day'
);

-- Create unique index that includes the partitioning column
-- This prevents duplicate posts while satisfying hypertable requirements
CREATE UNIQUE INDEX IF NOT EXISTS posts_unique_idx ON posts (unique_name, created_timestamp);
