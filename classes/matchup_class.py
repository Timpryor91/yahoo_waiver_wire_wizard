# -*- coding: utf-8 -*-
"""

@author: timpr
"""
from classes.player_class import Player
from classes.team_class import NBAteam

from yfpy.query import YahooFantasySportsQuery
import json
from datetime import datetime
from datetime import timedelta

class Matchup(object):
    """
    A fantasy matchup object represents the state of a matchup on a particular day, when a waiver player is needed 

    """
    def __init__(self, date, user_team_name, yahoo_query, game_id):
        """
        Initialize a fantasy matchup object
        
        Parameters:
            date (string): the date that the player needs to be streamed on, the tool should be run on the morning before streaming
            user_team_name (string): the name of the users team
            yahoo_query (YahooFantasySportsQuery): A Yahoo fantasy sports query object that can be used to retrieve all data from Yahoo fantasy

        """
        self.date = date
        self.user_team_name = user_team_name
        self.yahoo_query = yahoo_query
        self.game_id = game_id
        
    def get_matchup_end_date(self):
        """
        Determines the start date, end date and days remaining in the matchup
        
        Parameters:
            None
            
        Returns
            end_date (string): the last day of the matchup
            start_date (string): the first day of the matchup
            day_remaining (integer): the number of days remaining in the matchup
            current_Week (string): the current league week number
            
        """        
        self.schedule_weeks = self.yahoo_query.get_game_weeks_by_game_id(self.game_id)
        # Loop through the matchup weeks until the start date is before the current date to find current week
        for week in self.schedule_weeks:
            self.week_json = (json.loads(str(week["game_week"])))
            if datetime.strptime(self.week_json["end"],"%Y-%m-%d") > datetime.strptime(self.date,"%Y-%m-%d"):
                self.end_date = self.week_json["end"]
                return(self.end_date)
        
        raise Exception("Nominated date not in the league season")
        return
    
    def get_user_team_id(self):
        """
        Gets the team id of the user
        
        Parameters:
            None
            
        Returns:
            user_team_id: the id of the user's team
        
        """
        self.info_json = (json.loads(str(self.yahoo_query.get_league_info())))
        
        for team in self.info_json["standings"]["teams"]:
            if (team["team"]["name"] == self.user_team_name):
                return (team["team"]["team_id"])
        
        raise Exception("Team name not found in league info, please check spelling of team name.")
        return
        
    def get_opponent_id(self):
        """
        Gets the team id of the user's current opponent
        
        Parameters:
            None
            
        Returns
            opponent_id (string): the id of the opposing team in the matchup
        """ 
        
        self.user_team_id = self.get_user_team_id()
        self.info_json = (json.loads(str(self.yahoo_query.get_league_info())))
      
        for matchup in self.info_json["scoreboard"]["matchups"]:
            self.user_matchup = False
            self.matchup_teams = []
            for team in matchup["matchup"]["teams"]:
                self.matchup_teams.append(team["team"]["managers"]["manager"]["manager_id"])
                if (team["team"]["managers"]["manager"]["manager_id"] == self.user_team_id):
                    self.user_matchup = True
    
            if self.user_matchup == True:
                break
        
        if self.matchup_teams[0] == self.user_team_id:
            return(self.matchup_teams[1])
        else:
            return(self.matchup_teams[0])    
        
        raise Exception("No matchup found for users team this week.")
        return
                          
    def get_matchup_categories(self):
        """
        Determines the scoring categories for the matchup
        
        Returns:
            category_list (List<integer): the scoring categories for the matchup

        """        
        self.league_info_json = (json.loads(str(self.yahoo_query.get_league_info())))
        self.category_list = []
        for key in self.league_info_json["settings"]["stat_categories"]["stats"]:
            self.category_list.append((key["stat"]["display_name"]))
            
        return(self.category_list)
    
    def get_nba_team_abbr(self, nba_team_name):
        """
        Find the team abbreviation associated with an NBA team name
        
        Parameters:
            nba_team_name (string): The full name of an NBA team, consistent with yahoo fantasy library
        
        Returns:
            nba_team_abbr (string): The abbreviation of the NBA team, consistent with sportsipy library
        
        """
        self.nba_abbr_dict = {
                        "Atlanta Hawks":'ATL',
                        "Brooklyn Nets":'BRK',
                        "Boston Celtics":'BOS',
                        "Charlotte Hornets":'CHO',
                        "Chicago Bulls":'CHI',
                        "Cleveland Cavaliers":'CLE',
                        "Dallas Mavericks":'DAL',
                        "Denver Nuggets":'DEN',
                        "Detroit Pistons":'DET',
                        "Golden State Warriors":'GSW',
                        "Houston Rockets":'HOU',
                        "Indiana Pacers":'IND',
                        "Los Angeles Clippers":'LAC',
                        "Los Angeles Lakers":'LAL',
                        "Memphis Grizzlies":'MEM',
                        "Miami Heat":'MIA',
                        "Milwaukee Bucks":'MIL',
                        "Minnesota Timberwolves":'MIN',
                        "New Orleans Pelicans":'NOP',
                        "New York Knicks":'NYK',
                        "Oklahoma City Thunder":'OKC',
                        "Orlando Magic":'ORL',
                        "Philadelphia 76ers":'PHI',
                        "Phoenix Suns":'PHO',
                        "Portland Trail Blazers":'POR',
                        "Sacramento Kings":'SAC',
                        "San Antonio Spurs":'SAS',
                        "Toronto Raptors":'TOR',
                        "Utah Jazz":'UTA',
                        "Washington Wizards":'WAS'            
                        } 
        self.nba_team_abbr = self.nba_abbr_dict[nba_team_name]
        return(self.nba_team_abbr) 
           
    def get_nba_teams(self, date, end_date):  
        """
        Creates a list of nba team objects, containing all teams in the league
        
        Parameters:
            None
        
        Returns:
            nba_teams (Dict<string:NBAteam>): A dictionary of NBA team objects, with team names and schedules associated with them
    
        """
        self.nba_teams = {
                    'ATL': NBAteam('ATL',date, end_date),
                    'BRK': NBAteam('BRK',date, end_date),
                    'BOS': NBAteam('BOS',date, end_date),
                    'CHO': NBAteam('CHO',date, end_date),
                    'CHI': NBAteam('CHI',date, end_date),
                    'CLE': NBAteam('CLE',date, end_date),
                    'DAL': NBAteam('DAL',date, end_date),
                    'DEN': NBAteam('DEN',date, end_date),
                    'DET': NBAteam('DET',date, end_date),
                    'GSW': NBAteam('GSW',date, end_date),
                    'HOU': NBAteam('HOU',date, end_date),
                    'IND': NBAteam('IND',date, end_date),
                    'LAC': NBAteam('LAC',date, end_date),
                    'LAL': NBAteam('LAL',date, end_date),
                    'MEM': NBAteam('MEM',date, end_date),
                    'MIA': NBAteam('MIA',date, end_date),
                    'MIL': NBAteam('MIL',date, end_date),
                    'MIN': NBAteam('MIN',date, end_date),
                    'NOP': NBAteam('NOP',date, end_date),
                    'NYK': NBAteam('NYK',date, end_date),
                    'OKC': NBAteam('OKC',date, end_date),
                    'ORL': NBAteam('ORL',date, end_date),
                    'PHI': NBAteam('PHI',date, end_date),
                    'PHO': NBAteam('PHO',date, end_date),
                    'POR': NBAteam('POR',date, end_date),
                    'SAC': NBAteam('SAC',date, end_date),
                    'SAS': NBAteam('SAS',date, end_date),
                    'TOR': NBAteam('TOR',date, end_date),
                    'UTA': NBAteam('UTA',date, end_date),
                    'WAS': NBAteam('WAS',date, end_date)               
                    }
        
        return(self.nba_teams)
    
    
    def get_stat_id_dict(self):
        """
        Creates a dictionary that maps stat ids to stat names, needed for referencing purposes between different stat functions
        
        Parameters:
            None
        
        Returns:
            stat_id_dict (Dict<string:string>): a dictionary with stat IDs as keys, stat display names as values
        
        """
        self.stat_id_dict = {}
        self.stat_categories = (json.loads(str(self.yahoo_query.get_game_stat_categories_by_game_id(self.game_id))))

        for stat in self.stat_categories["stats"]:
            self.stat_id_dict[str(stat["stat"]["stat_id"])] = stat["stat"]["display_name"]
        
        return(self.stat_id_dict)
    
    def get_team_roster(self, team_id, category_list, stat_id_dict):
        """
        Determines the roster of a team
        
        Returns:
            team_roster (List<Player>): a list with all the players on a team

        """ 
        self.team_id = team_id
        self.category_list = category_list
        self.stat_id_dict = stat_id_dict
        self.team_roster = []
        self.team_info_json = (json.loads(str(self.yahoo_query.get_team_info(self.team_id))))
        
        for player in self.team_info_json["roster"]["players"]:
            self.player_name = player["player"]["name"]["full"]
            self.player_id = player["player"]["player_id"]
            self.nba_team = self.get_nba_team_abbr(player["player"]["editorial_team_full_name"])
            self.player_key = player["player"]["player_key"]
            if "status" in player["player"] and player["player"]["status"] != "GTD":
                self.is_injured = True
            else:
                self.is_injured = False
            self.team_roster.append(Player(self.player_name, 
                                           self.player_id, 
                                           self.nba_team, 
                                           self.team_id, 
                                           self.player_key, 
                                           self.category_list,
                                           self.stat_id_dict,
                                           self.yahoo_query,
                                           self.is_injured)
                                    )
        return (self.team_roster)
    
    def get_num_players_on_court(self):
        """
        Gets the number of players contributing to a teams score each night
        
        Returns:
            on_court_players(int): the number of players allowed on court 
                                                       
        """           
        self.on_court_players = 0
        self.team_info_json = (json.loads(str(self.yahoo_query.get_team_info(self.team_id))))  
        for player in self.team_info_json["roster"]["players"]:
            if player["player"]["selected_position"]["position"] != "BN":
                if player["player"]["selected_position"]["position"] != "IL":
                    self.on_court_players += 1
        
        return(self.on_court_players)
    
    def get_current_matchup_scores(self):
        """
        Gets the current matchup score based on user inputs
        
        Returns:
             matchup_scores (Dict<string:List<float>): a dictionary with stat categories as keys, 
                                                       a list with the score of each team as values
        """                     
        #TO DO
        self.matchup_scores = {
                              "FG%": [0.478, 0.456],
                              "FT%": [0.876, 0.912],
                              "3PTM": [45, 67],
                              "PTS": [145, 210],
                              "REB": [67, 98],
                              "AST": [34, 27],
                              "TO": [21, 31],
                              "ST": [13, 16],
                              "BLK": [9, 8]
                              }
        
        return(self.matchup_scores)
    
    
    def get_projected_scores(self):
        """
        Determines projected scores at the end of the matchup
        
        Returns:
            projected_scores (Dict<string:List<float>): a dictionary with stat categories as keys,
                                                        a list with the projected final score of each team as values

        """         
        # Get the rosters for each team and the current matchup score
        self.category_list = self.get_matchup_categories()
        self.stad_id_dict = self.get_stat_id_dict() 
        self.rosters = [self.get_team_roster(self.get_user_team_id(), self.category_list, self.stat_id_dict), 
                        self.get_team_roster(self.get_opponent_id(), self.category_list, self.stat_id_dict)]
        self.projected_scores = self.get_current_matchup_scores()
        self.end_date = self.get_matchup_end_date()
        self.nba_teams = self.get_nba_teams(self.date, self.end_date)
        self.players_on_court_limit = self.get_num_players_on_court()
        
        self.current_datetime = datetime.strptime(self.date,"%Y-%m-%d")
        self.end_datetime = datetime.strptime(self.end_date, "%Y-%m-%d")
        self.days_remaining = 0
        
        while self.current_datetime <= self.end_datetime:
            for roster in range(len(self.rosters)):
                self.players_on_court = 0
                for player in self.rosters[roster]:
                    # Check if player has a game on this day based on their team
                    self.player_nba_team = player.get_player_nba_team()
                    self.player_schedule = self.nba_teams[self.player_nba_team].get_schedule()
                    if datetime.strftime(self.current_datetime,"%Y-%m-%d") in self.player_schedule:
                        # Ensure not too many player scores are counted per day
                        self.players_on_court += 1
                        if self.players_on_court > self.players_on_court_limit:
                            break
                        
                        # Ensure the player is not injured
                        if player.get_injury_status():
                            break
                        
                        # Get the players average stats using the player class
                        player_stats = player.get_average_stats()
                        for stat in player_stats:
                            # Check to see if the stat is a counting stat or FG%/FT% 
                            # as needs to be added differently if so  
                            if stat == "FG%" or stat == "FT%":
                                self.projected_scores[stat][roster] = (30*self.projected_scores[stat][roster] + float(player_stats[stat]))/31
                            else:
                                self.projected_scores[stat][roster] += float(player_stats[stat])

            self.days_remaining += 1
            self.current_datetime += timedelta(days=1)
        
        return(self.projected_scores, self.days_remaining, self.nba_teams)
    
    def get_weighting_scores(self):
        """
        Calculates weighting scores based on the category margins and uncertainty correction factor (which is
        based on the number of days remaining in the matchup)
        
        Returns:
            weighting_scores (Dict<string:float): a dictionary with stat categories as keys,
                                                  weighting scores as values

        """           
        self.projected_scores, self.days_remaining, self.nba_teams = self.get_projected_scores()
        self.uncertainty_correction_factor_dict = {
                                                1:1,
                                                2:0.9,
                                                3:0.6,
                                                4:0.2
                                                }
        self.correction_factor = 0
        for days in self.uncertainty_correction_factor_dict:
            if self.days_remaining == days:
                self.correction_factor = self.uncertainty_correction_factor_dict[days]
        
        self.weighting_scores_factors = {
                                        0.03: 5,
                                        0.05: 3,
                                        0.10: 2,
                                        0.15: 1
                                        }
        self.weighting_scores = {}
        for stat in self.projected_scores:
            self.percentage_diff = self.correction_factor*abs(self.projected_scores[stat][0] - 
                                       self.projected_scores[stat][1])/self.projected_scores[stat][0]
            
        return(self.weighting_scores, self.nba_teams)
    