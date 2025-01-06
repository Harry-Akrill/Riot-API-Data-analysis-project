Riot API Data Analysis Project - 

Personal Project which utilises the Riot Games Developers API to conduct data analysis on a set of League of Legends games.

riot_data_functions.py allows you to pull data from the Riot Servers, according to an input name, server, queue type, and number of games you wish to retrieve. The data is then manipulated and cleaned according to a specific set of criteria.

import_to_sheets.py takes the data retrieved and imports it to a google sheets table, showing the averages of a players games, as well as a list of all of the players games.

matchup_analysis.py is an intial look into analysing specific 'champion' matchups, and utilises various python libraries to find correlations between specific in-game statistics, and the likelihood of them leading to a win.
