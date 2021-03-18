# -*- coding: utf-8 -*-
"""

@author: timpr
"""
from sportsipy.nba.schedule import Schedule
from datetime import datetime

class NBAteam(object):
    """
    A Team object represents an NBA team
    """    
    def __init__(self, nba_team_name, date, end_date):
        """
        Initialize an NBA team object.

        Parameters:
            team_name (string): name of the NBA team
            date (string): the day a player needs to be acquired for
            end_date (string): the last day of the matchup
            
        """
        self.nba_team_name = nba_team_name
        self.date = date
        self.end_date = end_date
        
        # Create schedule using sportsipy
        self.team_schedule = []
        self.schedule_object = Schedule(self.nba_team_name, year = int(self.date[0:4]))
        for game in self.schedule_object:
            self.game_datetime = datetime.strptime(game.date[5:],"%b %d, %Y")
            if datetime.strptime(self.date, "%Y-%m-%d") <= self.game_datetime and datetime.strptime(self.end_date, "%Y-%m-%d") >= self.game_datetime:
                self.team_schedule.append((self.game_datetime).strftime("%Y-%m-%d"))

    def get_schedule(self):
        return(self.team_schedule)
    
    def get_nba_team_name(self):    
        return (self.nba_team_name)