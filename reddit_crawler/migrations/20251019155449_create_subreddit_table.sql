-- Table: Subreddit
-- Stores basic metadata about subreddits on Reddit.

CREATE TABLE Subreddit (
    id SERIAL PRIMARY KEY,                       -- Unique ID for each subreddit
    unique_name TEXT Unique,                     -- This is a globally unique identifier for a subreddit
    title TEXT NOT NULL,                         -- Title of the subreddit (e.g., "Home")
    subscribers INTEGER NOT NULL DEFAULT 0,      -- Number of users subscribed
    description TEXT,                            -- Short description of the subreddit
    lang VARCHAR(10),                            -- Language code (e.g., "en")
    url TEXT NOT NULL UNIQUE,                    -- Subreddit path (e.g., "/r/Home/")
    created_utc DOUBLE PRECISION,                -- Original subreddit creation time (Unix UTC)
    icon_img TEXT,
    over18 BOOLEAN NOT NULL DEFAULT false,       -- True if marked NSFW (adult content)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()  -- When this row was added to the DB
);