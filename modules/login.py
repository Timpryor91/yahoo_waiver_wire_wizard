# -*- coding: utf-8 -*-
"""

@author: timpr
"""

from yfpy.query import YahooFantasySportsQuery

def yahoo_login(game_id, league_id, game_code):
    """
    Logins to account and queries data for league of interest
    
    Parameters:
        game_id (string): the id relating to the year and type of fantasy sport being player
        league_id (string): the unique id for a yahoo fantasy sports league
        game_code (string): the type of sport being player e.g. 'nba'
    
    Returns:
        yahoo_query (YahooFantasySportsQuery): A Yahoo fantasy sports query object that can be used to retrieve all data from Yahoo fantasy
    
    """
  
    # Change this directory to be the directory where you have your private.json file saved
    auth_dir = "C:/Users/timpr/Desktop/Tim Misc Docs/Coding/Personal Projects/Waiver Wire Wizard/waiver_wire_wizard/"

    yahoo_query = YahooFantasySportsQuery(
                                        auth_dir,
                                        league_id,
                                        game_id=game_id,
                                        game_code=game_code,
                                        offline=False,
                                        ) 
    return(yahoo_query)