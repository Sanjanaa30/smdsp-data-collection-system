-- Add up migration script here
--using https://a.4cdn.org/{board}/catalog.json

-- Table: threads
-- Purpose: Stores 4chan thread data.
    -- Track active threads from catalog.json
    -- Monitor thread activity and status
    -- Fast queries for thread discovery

CREATE TABLE threads (
    thread_id BIGINT NOT NULL PRIMARY KEY,      -- thread ID (no.)
    board_code TEXT NOT NULL,                   -- board identifier
    thread_title TEXT,                          -- thread title (subject)
    comment_texts TEXT,                         -- comment texts
    poster_name TEXT,                           -- poster name (name)
    created_time BIGINT,                        -- creation time (Unix timestamp)
    last_modified BIGINT,                       -- last modified time (Unix timestamp)
    replies INTEGER DEFAULT 0,                  -- no. of replies
    images INTEGER DEFAULT 0,                   -- no. of images
    semantic_url TEXT,                          -- semantic_url
    is_sticky BOOLEAN DEFAULT FALSE,            -- sticky 
    is_closed BOOLEAN DEFAULT FALSE,            -- closed
    country_code TEXT,                          -- country
    has_media BOOLEAN DEFAULT FALSE,            -- derived from filename != null
    
    -- Thread limits and metadata
    bump_limit INTEGER DEFAULT 0,               -- bumplimit
    image_limit INTEGER DEFAULT 0,              -- imagelimit  

    last_seen_in_catalog TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (board_code) REFERENCES boards(board_code)
);