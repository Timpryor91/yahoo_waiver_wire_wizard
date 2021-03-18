# -*- coding: utf-8 -*-
"""

@author: timpr
"""
from classes.player_class import Player
from classes.team_class import NBAteam

from nba_api.stats import endpoints as nba_api_endpoints
from nba_api.stats.static import players as nba_api_players
import json
from datetime import datetime
from datetime import timedelta
import operator

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
            game_id (string): the id of the fantasy game, currently 402 for the 2020,2021 NBA season, can be found using the yfpy 
                              get_all_yahoo_fantasy_game_keys() function
        
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
            user_team_id (string): the id of the user's team
        
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
            category_list (List<string>): the scoring categories for the matchup

        """        
        self.league_info_json = (json.loads(str(self.yahoo_query.get_league_info())))
        self.category_list = []
        for key in self.league_info_json["settings"]["stat_categories"]["stats"]:
            if key["stat"]["display_name"] == "FGM/A" or key["stat"]["display_name"] == "FTM/A":
                continue
            self.category_list.append((key["stat"]["display_name"]))
            
        return(self.category_list)
               
    def get_nba_teams(self, date, end_date):  
        """
        Creates a list of nba team objects, containing all teams in the league
        
        Parameters:
            date (string): the date that the player needs to be streamed on, the tool should be run on the morning before streaming (YY-MM-DD)
            end_date (string): the last day of the matchup (YY-MM-DD)
        
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
       
    def get_league_players(self):
        """
        Creates a list of all active players, using data from the nba_api
        
        Returns:
            league_players (List<Player>): a list of all players in the league
        
        """
        self.player_list = []
        self.player_name_list = []
        # Find nba_api player IDs for each player in the league (these IDs are different than yahoo fantasy IDs)
        for player in nba_api_players.get_active_players():
                self.player_name_list.append([player["full_name"],
                                          nba_api_players.find_players_by_full_name(player["full_name"])[0]["id"]])
      
        for player in self.player_name_list:
                    
            # Look up fantasy profile for player
            # nba_api calls can be unrealiable, so use exceptions to prevent code from crashing if a query fails
            try:
                self.player_profile = nba_api_endpoints.playerfantasyprofile.PlayerFantasyProfile(player[1])             
            except Exception:
                continue

            # Only add players who have at least played one game
            if (len(self.player_profile.get_dict()["resultSets"][0]["rowSet"]) != 0):
                # Find player's nba team
                try:
                    self.nba_team = nba_api_endpoints.playerprofilev2.PlayerProfileV2(player[1]).get_dict()["resultSets"][0]["rowSet"][-1][4]
                except Exception:
                    continue
                    
                # Create stat dictionary for player
                self.player_stat_list = self.player_profile.get_dict()["resultSets"][0]["rowSet"][0]    
                self.player_stat_dict = {
                                    "GP": float(self.player_stat_list[2]),
                                    "FG%": float(self.player_stat_list[9]),
                                    "FT%": float(self.player_stat_list[15]),
                                    "3PTM": float(self.player_stat_list[10])/float(self.player_stat_list[2]),
                                    "PTS": float(self.player_stat_list[26])/float(self.player_stat_list[2]),
                                    "REB": float(self.player_stat_list[18])/float(self.player_stat_list[2]),
                                    "AST": float(self.player_stat_list[19])/float(self.player_stat_list[2]),
                                    "TO": float(self.player_stat_list[20])/float(self.player_stat_list[2]),
                                    "ST": float(self.player_stat_list[21])/float(self.player_stat_list[2]),
                                    "BLK": float(self.player_stat_list[22])/float(self.player_stat_list[2]),
                                    "DD": float(self.player_stat_list[28])/float(self.player_stat_list[2]),
                                    "TD": float(self.player_stat_list[29])/float(self.player_stat_list[2])
                                    }
                
                # Infer if the player is injured by checking their most recent game, to avoid suggestions who are on the IR
                try:
                    self.recent_game = nba_api_endpoints.playergamelog.PlayerGameLog(player[1]).get_dict()["resultSets"][0]["rowSet"][0][3]
                    if (datetime.strptime(self.recent_game, "%b %d, %Y") + timedelta(days = 7)) < datetime.now():
                        self.is_injured = True
                    else:
                        self.is_injured = False
                except Exception:
                    self.is_injured = False
                    pass
 
                # Initiate player object to add into league player list
                self.player_list.append(Player(player[0],
                                               None,
                                               self.nba_team,
                                               None,
                                               None,
                                               self.player_stat_dict,
                                               self.is_injured))
        return(self.player_list)
    
    def get_team_roster(self, team_id, league_players):
        """
        Determines the roster of a team
        
        Parameters:
            team_id (string): the id of the team of interest
            league_players (List<Player>): a list of all players in the league
        
        Returns:
            team_roster (List<Player>): a list with all the players on a team

        """ 
        self.team_id = team_id
        self.team_roster = []
        self.league_players = league_players
        self.team_info_json = (json.loads(str(self.yahoo_query.get_team_info(self.team_id))))
        
        for player in self.team_info_json["roster"]["players"]:
            self.player_name = player["player"]["name"]["full"]
            self.player_id = player["player"]["player_id"]
            self.player_key = player["player"]["player_key"]
            if "status" in player["player"] and player["player"]["status"] != "GTD":
                self.is_injured = True
            else:
                self.is_injured = False
            
            # Find the player from the league list and update with additional details
            for league_player in self.league_players:
                if league_player.get_player_name() == self.player_name:
                    league_player.set_player_id(self.player_id)
                    league_player.set_player_fantasy_team_id(self.team_id)
                    league_player.set_player_key(self.player_key)
                    league_player.set_injury_status(self.is_injured)
                    self.team_roster.append(league_player)
                    break
                                                     
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
            
    def get_projected_scores(self, nba_teams, end_date, league_players, current_scores):
        """
        Determines projected scores at the end of the matchup
        
        Parameters:
            nba_teams (Dict<string:NBAteam>): A dictionary of NBA team objects, with team names and schedules associated with them
            end_date (string): the last day of the matchup
            league_players (List<Player>): a list of all players in the league
            current_scores (Dict<List<float>>): a dictionary with categories as keys, a list with the user score and opponent score for the
                                                category as values
        
        Returns:
            projected_scores (Dict<string:List<float>): a dictionary with stat categories as keys,
                                                        a list with the projected final score of each team as values
            days_remaining (integer): the number of days remaining in the matchup

        """         
        # Get the rosters for each team and the current matchup score
        self.league_players = league_players
        self.rosters = [self.get_team_roster(self.get_user_team_id(), self.league_players), 
                        self.get_team_roster(self.get_opponent_id(), self.league_players)]
        self.projected_scores = current_scores
        self.end_date = end_date
        self.nba_teams = nba_teams
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
                            # Check if the particular stat is counted in the league format
                            if stat in self.projected_scores:
                                # Check to see if the stat is a counting stat or FG%/FT% 
                                # as needs to be added differently if so  
                                if stat == "FG%" or stat == "FT%":
                                    self.projected_scores[stat][roster] = (30*self.projected_scores[stat][roster] + float(player_stats[stat]))/31
                                else:
                                    self.projected_scores[stat][roster] += float(player_stats[stat])

            self.days_remaining += 1
            self.current_datetime += timedelta(days=1)
        
        return(self.projected_scores, self.days_remaining)
    
    def get_weighting_scores(self, projected_scores, days_remaining):
        """
        Calculates weighting scores based on the category margins and uncertainty correction factor (which is
        based on the number of days remaining in the matchup)
        
        Parameters:
            projected_scores (Dict<string:List<float>): a dictionary with stat categories as keys,
                                                        a list with the projected final score of each team as values
            days_remaining (integer): the number of days remaining in the matchup            
        
        Returns:
            weighting_scores (Dict<string:float): a dictionary with stat categories as keys,
                                                  weighting scores as values

        """           
        self.projected_scores = projected_scores
        self.days_remaining = days_remaining
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
            
        return(self.weighting_scores)

    def get_waiver_player_list(self, league_players):
        """
        Find the available players on the waivers by removing all the owned players from the overall player list
        
        Parameters:
            league_players (List<Player>): a list of all players in the league
        
        Returns:
            waiver_players(List<Player>): A list of players that are available for acquisition from the waivers

        """           
        self.league_players = league_players
        self.waiver_player_list = self.league_players.copy()
        self.num_teams = (json.loads(str(self.yahoo_query.get_league_metadata())))["num_teams"]
        
        # Remove all of the players that are already on a team from the waiver player list
        for i in range(1, self.num_teams + 1):
            self.team_roster = self.get_team_roster(str(i), self.league_players)
            for player in self.team_roster:     
                self.waiver_player_list.remove(player)
        
        return(self.waiver_player_list)

    def get_waiver_scores(self, waiver_player_list, weighting_scores):
        """
        Calculates the viability score for all players in the waiver players list.
        
        Parameters:
            waiver_players(List<Player>): A list of players that are available for acquisition from the waivers
            weighting_scores (Dict<string:float): a dictionary with stat categories as keys,
                                                  weighting scores as values
        
        Returns:
            waiver_player_scores(List<Tuple<string,float>): a sorted list of tuples, each tuple containing a player name 
                                                            and their waive score 

        """           
        self.waiver_player_list = waiver_player_list
        self.weighting_scores = weighting_scores
        self.waiver_player_scores = {}
        
        # Raw scoring system, based on points league format
        self.scoring_system = {
                              "FG%": 0,
                              "FT%": 0,
                              "3PTM": 3,
                              "PTS": 0.5,
                              "REB": 1.5,
                              "AST": 2,
                              "TO": -2,
                              "ST": 3,
                              "BLK": 3,
                              "DD": 4,
                              "TD": 5
                                }
        
        for player in self.waiver_player_list:
            
            # Don't calculate scores for injured players
            if player.get_injury_status():
                continue
            
            self.player_stats = player.get_average_stats()
            self.player_score = 0
            for stat in self.player_stats:
                if stat in self.scoring_system:
                    self.player_score += self.player_stats[stat]*self.scoring_system[stat]
            
            # Factor scores based on on fg and ft %s
            if self.player_stats["FG%"] < 0.45:
                self.player_score *= 0.9
            elif self.player_stats["FG%"] < 0.47:
                self.player_score *= 0.95
            elif self.player_stats["FG%"] > 0.55:
                self.player_score *= 1.10
            elif self.player_stats["FG%"] > 0.525:
                self.player_score *= 1.05

            if self.player_stats["FT%"] < 0.75:
                self.player_score *= 0.9
            elif self.player_stats["FT%"] < 0.80:
                self.player_score *= 0.95
            elif self.player_stats["FT%"] > 0.90:
                self.player_score *= 1.10
            elif self.player_stats["FT%"] > 0.85:
                self.player_score *= 1.05
           
            self.waiver_player_scores[player.get_player_name()] = round(self.player_score,2)
        
        # Sort the dictionary into order based on player viability scores
        self.sorted_waiver_player_scores  = sorted(self.waiver_player_scores.items(), key = operator.itemgetter(1), reverse = True)
                
        return(self.sorted_waiver_player_scores)