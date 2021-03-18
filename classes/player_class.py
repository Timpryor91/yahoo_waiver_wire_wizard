# -*- coding: utf-8 -*-
"""

@author: timpr
"""
class Player(object):
    """
    An NBA player object, associated with a particular fantasy league in a particular week
    """    
    def __init__(self, player_name, player_id, nba_team, team_id, player_key, 
                 stat_dict, is_injured):
        """
        Initialize an NBA team object

        Parameters:
            player_name (string): name of the player
            player_id (string): the players unique id, used to look up player in yahoo queries
            nba_team (NBAteam): the NBA team that the player is on
            team_id (string): the name of the fantasy team that the player is on (None if on the waivers)
            player_key (string): the players unique key, used to look up player in some yahoo queries
            stat_dict (Dict<string,float): A dictionary containing a players average stats, statistical category as key, average as value
            is_injured (Boolean): True if the player is injured and not playing, False otherwise
        """
        
        # Convert acronyms to match the format from Sportsipy
        if nba_team == "BKN":
            self.nba_team = "BRK"
        elif nba_team == "CHA":
            self.nba_team = "CHO"
        elif nba_team == "PHX":
            self.nba_team = "PHO"
        elif nba_team == "TOT":
            self.nba_team = "TOR"
        else:
            self.nba_team = nba_team
        
        self.player_name = player_name
        self.team_id = team_id
        self.player_id = player_id
        self.player_key = player_key
        self.stat_dict = stat_dict
        self.is_injured = is_injured
    
    def set_player_id(self, player_id):
        self.player_id = player_id
        return
    
    def set_player_fantasy_team_id(self, team_id):
        self.team_id = team_id
        return
    
    def set_player_key(self, player_key):
        self.player_key = player_key
        return
        
    def set_injury_status(self, is_injured):
        self.is_injured = is_injured
        return
                 
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
        return(self.stat_dict)
    
    def get_injury_status(self):
        return(self.is_injured)
    

    