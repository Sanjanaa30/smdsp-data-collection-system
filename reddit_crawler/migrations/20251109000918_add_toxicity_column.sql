-- Add migration script here
-- migrations/20251109000918_add_toxicity_column.sql

CREATE TABLE IF NOT EXISTS toxicity (
  unique_name      TEXT    NOT NULL,         -- Reddit post/comment ID (e.g., 't3_1oyvlqa', 't1_xyz')
  titleOrComment   TEXT    NOT NULL, 
  subreddit        TEXT    NOT NULL,         -- e.g., 'technology', 'sports'
  comment          TEXT    NOT NULL,         -- Post comment/content (HTML formatted)
  scored_at        TIMESTAMPTZ NOT NULL DEFAULT now(), -- timestamp when the toxicity scores were computed
  language         TEXT,                     -- e.g., 'en', 'es' - language of the comment

  toxicity         REAL CHECK (toxicity BETWEEN 0 AND 1),        -- overall toxicity score
  severe_toxicity  REAL CHECK (severe_toxicity BETWEEN 0 AND 1), -- severe toxicity score
  identity_attack  REAL CHECK (identity_attack BETWEEN 0 AND 1), -- identity attack score
  insult           REAL CHECK (insult BETWEEN 0 AND 1),          -- insult score
  threat           REAL CHECK (threat BETWEEN 0 AND 1),          -- threat score
  profanity        REAL CHECK (profanity BETWEEN 0 AND 1),       -- profanity score
  sexually_explicit REAL CHECK (sexually_explicit BETWEEN 0 AND 1), -- sexually explicit score
  flirtation       REAL CHECK (flirtation BETWEEN 0 AND 1),      -- flirtation score
  obscene          REAL CHECK (obscene BETWEEN 0 AND 1),         -- obscene score
  spam             REAL CHECK (spam BETWEEN 0 AND 1),            -- spam score
  unsubstantial    REAL CHECK (unsubstantial BETWEEN 0 AND 1),   -- unsubstantial score
  
  PRIMARY KEY (subreddit, unique_name)
);
