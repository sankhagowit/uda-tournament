#Getting Started
1. Open psql when inside of the directory containing this README and import the file 'tournament.sql' with the command:
    * \i tournament.sql
2. Activate python and import the file tournament.py to utilize the various functions for the swiss pairing tournament such as:
    * Add a player with registerPlayer(PlayerName)
    * Report the outcome of a pairing with reportMatch(winnerID, loserID)
    * See the standing of the tournament with playerStandings()
    * See the next round of swiss pairings with swissPairings()
    * Reset the win records with deleteMatches & players with deletePlayers
