-- Add up migration script here
-- migrations/20251024033313_posts.up.sql
-- =============================================
-- Migration: posts
-- Purpose:   Creates the `posts` table to store 4chan thread post data.
-- =============================================

CREATE TABLE IF NOT EXISTS posts (
    board_name TEXT,                       -- Name of the board (e.g., pol, b, etc.)
    post_no BIGINT NOT NULL,               -- Original 4chan post number (unique per thread)
    name TEXT,                             -- Name of the poster
    subject TEXT,                          -- Thread subject or title
    comment TEXT,                          -- Post comment/content (HTML formatted)
    filename TEXT,                         -- Original filename of the uploaded image
    ext TEXT,                              -- File extension (e.g., .png, .jpg)
    post_time BIGINT,                      -- Unix timestamp of when the post was made
    resto BIGINT,                          -- Parent thread number (0 if OP)
    country TEXT,                          -- Poster’s country code
    country_name TEXT,                     -- Poster’s full country name
    replies INT DEFAULT 0,                 -- Number of replies in the thread
    images INT DEFAULT 0,                  -- Number of images posted
    archived BOOLEAN DEFAULT FALSE,        -- Whether the thread/post is archived
    bumplimit BOOLEAN DEFAULT FALSE,       -- Whether the thread hit bump limit
    archived_on BIGINT,                    -- Unix timestamp when thread was archived
    created_at TIMESTAMP DEFAULT NOW()     -- Timestamp when the record was added to DB
);


SELECT create_hypertable(
    'posts',
    'created_at',
    chunk_time_interval => INTERVAL '1 hours'
);

CREATE UNIQUE INDEX IF NOT EXISTS posts_unique_idx ON posts (board_name, post_no, created_at);