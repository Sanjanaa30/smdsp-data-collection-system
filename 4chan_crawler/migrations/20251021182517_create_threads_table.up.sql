-- Add up migration script here

-- Table: threads
-- Purpose: Stores 4chan thread data.

CREATE TABLE threads (
    thread_id BIGINT NOT NULL PRIMARY KEY,      -- Unique identifier for the thread
    board_code TEXT NOT NULL,                   -- The board the thread belongs to
    thread_title TEXT,                          -- The title of the thread (can be NULL)
    com TEXT,                                   -- The comment text of the thread
    created_time INTEGER,              -- Unix timestamp when thread was created
    last_modified INTEGER,                      -- Unix timestamp of last activity
    replies INTEGER NOT NULL DEFAULT 0,         -- Total number of replies
    semantic_url TEXT,                          -- Readable thread link
    images INTEGER DEFAULT 0,                   -- Number of images in thread
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- When record was inserted
    FOREIGN KEY (board_code) REFERENCES boards(board_code)  -- Link to boards table
);