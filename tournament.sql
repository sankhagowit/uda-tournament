-- Automate database creation
-- Table definitions for the tournament project.
-- player table containing id, name, wins initialized at zero and matches
-- initialized at zero.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
    id serial primary key,
    name text
);

CREATE TABLE matches (
    match serial primary key,
    winner integer references players (id),
    loser integer references players (id)
);

CREATE VIEW wins AS
SELECT players.id, count(matches) AS wins
FROM players LEFT JOIN matches
ON players.id = matches.winner
GROUP BY players.id
ORDER BY wins DESC;

CREATE VIEW losses AS
SELECT players.id, count(matches) AS losses
FROM players LEFT JOIN matches
ON players.id = matches.loser
GROUP BY players.id
ORDER BY losses ASC;

CREATE VIEW summary AS
SELECT wins.id, wins.wins as wins, wins.wins+losses.losses AS matches
FROM wins LEFT JOIN losses
ON wins.id = losses.id
ORDER BY wins DESC;

-- Am I approaching the aggregation of the matches table correctly with the
-- creation of 4 views? Seems like I've added more code than "keeping count"
-- within the python module. I see how I could use a subqueries to wrap the
-- current wins and losses table into the summary but that doesn't involve
-- fewer lines of code.
CREATE VIEW standings AS
SELECT players.id, players.name, summary.wins, summary.matches
FROM players LEFT JOIN summary
ON players.id = summary.id
ORDER BY wins DESC;
