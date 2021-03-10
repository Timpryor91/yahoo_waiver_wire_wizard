# -*- coding: utf-8 -*-
"""

@author: timpr
"""
from classes.team_class import NBAteam

from yfpy.query import YahooFantasySportsQuery
import json
from nba_api.stats import endpoints as nba_api_endpoints
from nba_api.stats.static import players as nba_api_players


class Player(object):
    """
    An NBA player object, associated with a particular fantasy league in a particular week
    """    
    def __init__(self, player_name, player_id, nba_team, team_id, player_key, 
                 category_list, stat_id_dict, yahoo_query, is_injured):
        """
        Initialize an NBA team object

        Parameters:
            player_name (string): name of the player
            nba_team (NBAteam): the NBA team that the player is on
            average_stats (Dict<string,float): A dictionary containing a players average stats, statistical category as key, average as value
            team_id (string): the name of the fantasy team that the player is on (None if on the waivers)
            player_id (string): the players unique id, used to look up player in yahoo queries
            player (key): the players unique key, used to look up player in some yahoo queries
            category_list (List<string>): the scoring categories for the matchup
            stat_id_dict (Dict<string:string>): a dictionary with stat IDs as keys, stat display names as values
        """
        self.nba_team = nba_team
        self.player_name = player_name
        self.team_id = team_id
        self.player_id = player_id
        self.player_key = player_key
        self.category_list = category_list
        self.stat_id_dict = stat_id_dict
        self.yahoo_query = yahoo_query
        self.is_injured = is_injured
        
        # Calculate the players average stats for the season for the matchups categories
        # Games played data not available directly from yfpy so need to obtain from nba_api
        self.nba_api_player_id = nba_api_players.find_players_by_full_name(self.player_name)[0]["id"]
        self.nba_api_profile = nba_api_endpoints.playerfantasyprofile.PlayerFantasyProfile(self.nba_api_player_id)
        self.season_games_played = self.nba_api_profile.get_dict()["resultSets"][0]["rowSet"][0][2]

        self.player_stat_dict = {}                        
        self.player_stats = (json.loads(str(yahoo_query.get_player_stats_for_season(player_key))))
        
        for key in self.player_stats["player_stats"]["stats"]:
            if key["stat"]["stat_id"] not in self.stat_id_dict or self.stat_id_dict[key["stat"]["stat_id"]] not in self.category_list:
                continue
            elif (self.stat_id_dict[key["stat"]["stat_id"]] == "FG%" or self.stat_id_dict[key["stat"]["stat_id"]] == "FT%"):
                self.player_stat_dict[self.stat_id_dict[key["stat"]["stat_id"]]] = key["stat"]["value"]
            else:
                self.player_stat_dict[self.stat_id_dict[key["stat"]["stat_id"]]] = float(key["stat"]["value"])/self.season_games_played
  
    def get_player_name(self):
        return(self.player_name)
    
    def get_player_id(self):
        return(self.player_id)
    
    def get_player_nba_team(self):
        return(self.nba_team)

    def get_player_fantasy_team_id(self):
        return(self.team_id)
    
    def get_player_key(self):
        return(self.player_key)
    
    def get_average_stats(self):
        return(self.player_stat_dict)
    
    def get_injury_status(self):
        return(self.is_injured)
    