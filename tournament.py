#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("UPDATE players SET wins = 0, matches = 0;")
    db.commit() # Do I need this for the delete?
    cursor.close() # All the examples have this line in addition to db.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit() # Do I need this for the delete?
    cursor.close() # All the examples have this line in addition to db.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM players;")
    output = cursor.fetchone()
    cursor.close()
    db.close()
    return output[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    clean_name = bleach.clean(name)
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (clean_name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM players ORDER BY wins DESC;""")
    output = cursor.fetchall()
    db.close()
    return output


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM players WHERE id = %s OR id = %s;", (winner, loser))
    output = cursor.fetchall() # wins index 2, matches index 3
    winnerWins = output[0][2] + 1
    winnerMatches = output[0][3] + 1
    loserMatches = output[1][3] + 1

    cursor.execute("UPDATE players SET wins = %s, matches = %s WHERE id = %s;", (winnerWins, winnerMatches, winner))
    db.commit()
    cursor.execute("UPDATE players SET matches = %s WHERE id = %s;", (loserMatches, loser))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM players ORDER BY wins DESC")
    output = cursor.fetchall()
    matches = len(output)/2
    swissPairings = []
    for x in range(0, matches):
        pairing = (output[2*x][0], output[2*x][1], output[2*x+1][0], output[2*x+1][1])
        swissPairings.append(pairing)
    return swissPairings
