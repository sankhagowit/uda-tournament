-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
--
--

-- player table containing id, name, wins initialized at zero and matches
-- initialized at zero.
CREATE TABLE players (
    id serial primary key,
    name text,
    wins integer,
    rounds integer
);

CREATE TABLE matches (
    round integer,
    home integer,
    away integer,
    winner integer,
);
