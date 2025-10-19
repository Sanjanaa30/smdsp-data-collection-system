-- Add up migration script here

-- Table: boards
-- Purpose: Stores metadata for each 4chan board.

CREATE TABLE boards (
    board_code TEXT NOT NULL PRIMARY KEY,       -- Unique short code for the board 
    board_title TEXT NOT NULL,                  -- Full display title of the board 
    meta_description TEXT,                      -- Short description of the board’s content and purpose
    ws_board INT NOT NULL,                  -- Not a work-safe board (NSFW): TRUE = SFW, FALSE = NSFW
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
);
