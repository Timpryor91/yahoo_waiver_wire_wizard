# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import tkinter as tk
import logging

from classes.matchup_class import Matchup
from modules.login import yahoo_login



class Interface(object):
    """
    Initiates an instance of a login interface object
    """
    
    def __init__(self, window):
        
        self.window = window        
        
        # Set heading
        self.window.title("Yahoo Fantasy Basketball Waiver Wire Wizard")
    
        # Create frames to position widgets
        self.frame_top = tk.Frame(bg= "#9966CC")
        self.frame_middle = tk.Frame(bg = "#9966CC")
        self.frame_bottom = tk.Frame(bg = "#9966CC")
        
        # Date field
        self.date_var = tk.StringVar()
        self.date_label = tk.Label(master = self.frame_top, text = "Date (YY-MM-DD)", bg="#9966CC", width = 30)
        self.date_entry = tk.Entry(master = self.frame_middle, width = 35, textvariable = self.date_var)
        
        # Team name field
        self.team_name_var = tk.StringVar()
        self.team_name_label = tk.Label(master = self.frame_top, text = "Team Name", bg="#9966CC", width = 30)
        self.team_name_entry = tk.Entry(master = self.frame_middle, width = 35, textvariable = self.team_name_var)
        
        # League ID field
        self.league_id_var = tk.StringVar()
        self.id_label = tk.Label(master = self.frame_top, text = "League ID", bg="#9966CC", width = 30)
        self.id_entry = tk.Entry(master = self.frame_middle, width = 35, textvariable = self.league_id_var)
            
        # Button to trigger login
        self.login_button = tk.Button(master = self.frame_bottom,
                                    command = self.login,
                                    height = 1,
                                    width = 8,
                                    text = "Login",
                                    )        
        
        # Pack widgets and frames
        self.date_label.pack(side = tk.LEFT)
        self.date_entry.pack(side = tk.LEFT)
        self.team_name_label.pack(side = tk.LEFT)
        self.team_name_entry.pack(side = tk.LEFT)
        self.id_label.pack(side = tk.LEFT)
        self.id_entry.pack(side = tk.LEFT)
        self.login_button.pack(side = tk.RIGHT, anchor = "se")  
        self.frame_top.pack()
        self.frame_middle.pack()
        self.frame_bottom.pack()
        
        
        # self.mainloop()
        
    def login(self):
        """
        Logs in to fantasy basketball league and prompts program to start, triggering category
        input fields
        """    
        
        # Suppress YahooFantasySportsQuery debug logging
        logging.getLogger("yfpy.query").setLevel(level=logging.INFO)
        
        self.date = self.date_var.get()
        self.user_team_name = self.team_name_var.get()
        self.league_id = self.league_id_var.get()
        self.game_id = "402"
        self.game_code = "nba"
        
        self.date = "2021-03-17"
        self.user_team_name = "Tim's Top-Notch Team"
        self.game_id = "402"
        self.game_code = "nba"
        self.league_id = '254983'
        
        # Login to Yahoo fantasy API
        self.yahoo_query = yahoo_login(self.game_id, self.league_id, self.game_code)
        
        # Create matchup
        self.todays_matchup = Matchup(self.date, self.user_team_name, self.yahoo_query, self.game_id)
        
        # Extract variables from matchup required to determine score projections
        self.end_date = self.todays_matchup.get_matchup_end_date()
        self.nba_teams = self.todays_matchup.get_nba_teams(self.date, self.end_date)
        self.category_list = self.todays_matchup.get_matchup_categories()
        
        # Add additional input cells to interface to get matchup scores from user
        self.frame_category = tk.Frame(bg= "#9966CC")
        self.matchup_heading_label = tk.Label(master = self.frame_category, text = "Current Matchup Scores", bg="#9966CC", width = 92, height = 2)
        self.user_team_name_label = tk.Label(master = self.frame_category, text = "Your Score", bg="#9966CC", width = 46)
        self.opponent_team_name_label = tk.Label(master = self.frame_category, text = "Opposition Score", bg="#9966CC", width = 46)
        self.matchup_heading_label.pack()
        self.frame_category.pack()
        self.user_team_name_label.pack(side = tk.LEFT)
        self.opponent_team_name_label.pack(side = tk.LEFT)
        
        # Add in entry cells and create string variables to allow for extraction of user entries
        self.category_stringvar_dict = {}
        for category in self.category_list:
            self.category_stringvar_dict[category] = self.add_category_entry_widgets(category)
        
        # Button to run tool
        self.frame_run_button = tk.Frame(bg= "#9966CC")
        self.run_button = tk.Button(master = self.frame_run_button,
                                    command = self.rank_players,
                                    height = 1,
                                    width = 20,
                                    text = "Get Waiver Players",
                                    )
        self.run_button.pack()
        self.frame_run_button.pack()
        
        return
        
    def add_category_entry_widgets(self, category_name):
        """
        Adds in cells to frame for the entry of category scores
        
        Parameters:
            category_name (string): the name of the category to enter
            frame (Frame): the frame to pack the entries into
        
        Returns:
            user_entry_var (tk.StringVar): A string variable for the user team's category score
            opp_entry_var (tk.StringVar): A string variable for the user team's category score
        """            
        self.category_name = category_name
        self.stat_frame = tk.Frame(bg= "#9966CC")
        
        self.user_entry_var = tk.StringVar()
        self.opp_entry_var = tk.StringVar()
        self.left_spacer = tk.Label(master = self.stat_frame, text = "", bg="#9966CC", width = 14)
        self.stat_user_entry = tk.Entry(master = self.stat_frame, width = 20, textvariable = self.user_entry_var)
        self.stat_label = tk.Label(master = self.stat_frame, text = self.category_name, bg="#9966CC", width = 27)
        self.stat_opp_entry = tk.Entry(master = self.stat_frame, width = 20, textvariable = self.opp_entry_var)
        self.right_spacer = tk.Label(master = self.stat_frame, text = "", bg="#9966CC", width = 14)
        self.left_spacer.pack(side = tk.LEFT)
        self.stat_user_entry.pack(side = tk.LEFT)
        self.stat_label.pack(side = tk.LEFT)
        self.stat_opp_entry.pack(side = tk.LEFT)
        self.right_spacer.pack(side = tk.LEFT)
        self.stat_frame.pack()
                                
        return([self.user_entry_var, self.opp_entry_var])
            
            
    def rank_players(self):
        """
        Runs the player prioritization algorithm and outputs the best player options to the interface
        
        Parameters:
            current_scores (Dict<string:List<float>): a dictionary with stat categories as keys, 
                                                      a list with the score of each team as values
        
        """
        # Add heading for output box
        self.frame_results = tk.Frame(bg= "#9966CC")
        self.results_heading_label = tk.Label(master = self.frame_results, text = "Recommended Players", bg="#9966CC", width = 92, height = 2)
        
        # Get current scores based on user entries
        self.current_scores = {}
        for category in self.category_stringvar_dict:
            self.current_scores[category] = [float(self.category_stringvar_dict[category][0].get()),
                                             float(self.category_stringvar_dict[category][1].get())]
        
        # Get league player list using nba_api
        self.league_players = self.todays_matchup.get_league_players()

        # Get projected matchup scores
        self.projected_scores, self.days_remaining = self.todays_matchup.get_projected_scores(self.nba_teams, 
                                                                         self.end_date, 
                                                                         self.league_players,
                                                                         self.current_scores)
        
        # Determine weighting values
        self.weighting_scores = self.todays_matchup.get_weighting_scores(self.projected_scores, self.days_remaining)
        
        # Rank waiver players
        self.waiver_player_list = self.todays_matchup.get_waiver_player_list(self.league_players)    
        self.waiver_player_scores = self.todays_matchup.get_waiver_scores(self.waiver_player_list, self.weighting_scores)
  
        # Output list of the top 5 players
        self.waiver_output_window = tk.Text(master = self.frame_results, width=60, height=6)
        for i in range(5):
            self.waiver_output_window.insert(tk.END, self.waiver_player_scores[i][0] + ": " + str(self.waiver_player_scores[i][1]) + " pts\n")

        
        self.results_heading_label.pack()
        self.waiver_output_window.pack()
        self.frame_results.pack()