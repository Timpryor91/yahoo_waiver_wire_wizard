# -*- coding: utf-8 -*-
"""

@author: timpr
"""

from yfpy.query import YahooFantasySportsQuery
import json

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

yahoo_query = yahoo_login("402",'254983',"nba")

team_info_json = (json.loads(str(yahoo_query.get_team_info("1"))))

for player in team_info_json["roster"]["players"]:
    if "status" in player["player"]:
        print(player["player"]["status"])

# for player in team_info_json["roster"]["players"]:
#     print(player["player"]["selected_position"]["position"])
#     print("")

# stat_id = {'0': 'GP', '1': 'GS', '2': 'MIN', '3': 'FGA', '4': 'FGM', '5': 'FG%', '6': 'FTA', '7': 'FTM', '8': 'FT%', '9': '3PTA', '10': '3PTM', '11': '3PT%', '12': 'PTS', '13': 'OREB', '14': 'DREB', '15': 'REB', '16': 'AST', '17': 'ST', '18': 'BLK', '19': 'TO', '20': 'A/T', '21': 'PF', '22': 'DISQ', '23': 'TECH', '24': 'EJCT', '25': 'FF', '26': 'MPG', '27': 'DD', '28': 'TD'}

# player_key = "402.p.4563"

# player_stats = (json.loads(str(yahoo_query.get_player_stats_for_season(player_key))))

# player_stat_dict = {}

# games_played = 30

# print("")
# for key in player_stats["player_stats"]["stats"]:
#     if key["stat"]["stat_id"] not in stat_id:
#         continue
#     elif (stat_id[key["stat"]["stat_id"]] == "FG%" or stat_id[key["stat"]["stat_id"]] == "FT%"):
#         player_stat_dict[stat_id[key["stat"]["stat_id"]]] = key["stat"]["value"]
#     else:
#         player_stat_dict[stat_id[key["stat"]["stat_id"]]] = float(key["stat"]["value"])/games_played
    
# print(player_stat_dict)

# player_data = open("player_Data.txt","w")
# for key in player_stats:
#     player_data.write(str(player_stats[key])+"\n")
# player_data.close()


# print("")
# for stat in player_stats["player_stats"]:    
#     print(stat)

