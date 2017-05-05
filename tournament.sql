-- Automate database creation
-- Table definitions for the tournament project.
-- player table containing id, name, wins initialized at zero and matches
-- initialized at zero.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
    id serial primary key,
    name text,
    wins integer DEFAULT 0,
    matches integer DEFAULT 0
);

CREATE TABLE matches (
    match serial primary key,
    winner integer references players (id),
    loser integer references players (id),
);
