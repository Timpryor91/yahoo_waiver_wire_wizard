# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import logging
from classes.matchup_class import Matchup
from classes.player_class import Player
from classes.team_class import NBAteam

from modules.login import yahoo_login
from modules.nba_teams import get_nba_teams
from modules.waiver_list import get_waiver_list
#from modules.waiver_scores import calculate_waiver_scores
from modules.best_players import print_best_players

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# User inputs
date = "2021-03-09"
user_team_name = "Tim's Top-Notch Team"
game_id = "402"
game_code = "nba"
league_id = '254983'

# Initiate interface to determine login details
# TO DO

# Login to Yahoo fantasy API
yahoo_query = yahoo_login(game_id, league_id, game_code)

# Create matchup
todays_matchup = Matchup(date, user_team_name, yahoo_query, game_id)

# Initiate interface for user to enter matchup statistics into
# TO DO

# Determine weighting values
category_weightings, nba_teams = todays_matchup.get_weighting_scores()

# Rank waiver players



# Get waiver list
#waiver_list = get_waiver_list()

# Calculate scores for players on the waivers
#waiver_scores = calculate_waiver_scores(waiver_list, weighting_scores)

# Output list of the top 5 players
#best_players = print_best_players(waiver_scores)
