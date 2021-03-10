# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 07:33:35 2021

@author: timpr
"""

import tkinter as tk

from modules.style_list import get_style_list

def initiate_login_interface():
    """
    Initiates an instance of the login interface for the program
     
    Returns:
        None
    """
    def classify():
        """
        Creates a plot showing where a beer rating falls on its normal distribution
        """    
        # TEMP PLACEHOLDER EXAMPLE CODE
        
        # Calculate beer style rating and populate results cell
        beer_rating = float(beer_rating_entry.get())
        if (beer_rating < style_avgs[current_style.get()] - 1.5*style_stdevs[current_style.get()]):
            style_rating_string.set("Poor")
            style_rating_label.config(bg = "#da9694")
        elif (beer_rating < style_avgs[current_style.get()] - 0.5*style_stdevs[current_style.get()]):
            style_rating_string.set("Subpar")
            style_rating_label.config(bg = "#fabf8f")
        elif (beer_rating < style_avgs[current_style.get()] + 0.5*style_stdevs[current_style.get()]):
            style_rating_string.set("Good")
            style_rating_label.config(bg = "#95b3d7")
        elif (beer_rating < style_avgs[current_style.get()] + 1.5*style_stdevs[current_style.get()]):
            style_rating_string.set("Very Good")
            style_rating_label.config(bg = "#c4d79b")
        else:
            style_rating_string.set("Excellent")
            style_rating_label.config(bg = "#92d050")
        
        # Clear the plot if it already exists
        # (need to do this to prevent generation of multiple graph instances)    
        beer_plot.clear()
        
        # Replot the average beer distribution after clearing full plot
        beer_plot.plot(x_all_beer, stats.norm.pdf(x_all_beer, all_beers[0], all_beers[1]))
        beer_plot.set_yticklabels([" ", " ", " ", " "])
        
        # Create distribution plot for current selected style
        avg_current = style_avgs[current_style.get()]
        stdev_current = style_stdevs[current_style.get()]
        x_current_style = np.linspace(avg_current - 3*stdev_current, avg_current + 3*stdev_current, 100)
        beer_plot.plot(x_current_style, stats.norm.pdf(x_current_style, avg_current, stdev_current))
        
        # Plot vertical line corresponding to the selected beer's rating
        beer_plot.plot([beer_rating, beer_rating], [0,stats.norm.pdf(beer_rating, avg_current, stdev_current)])
        
        # Update plots    
        graph_canvas.draw()
                       
        return
    
    # Create interface window
    window =tk.Tk()
    window.wm_title("Untappd Style Rating Adjustment")

    # Create frames to position widgets
    frame_top = tk.Frame(bg= "gold")
    frame_middle = tk.Frame(bg = "white")
    frame_bottom = tk.Frame(bg = "gold")
    frame_top_left = tk.Frame(master = frame_top, bg= "gold")
    frame_top_middle = tk.Frame(master = frame_top, bg= "gold")
    frame_top_right = tk.Frame(master = frame_top, bg= "gold")
    frame_middle_upper = tk.Frame(master = frame_middle, bg= "gold")
    frame_middle_lower = tk.Frame(master = frame_middle, bg= "white")
    
    # Beer name entry
    beer_name_label = tk.Label(master = frame_top_left, text = "Beer Name", bg="gold", width = 30)
    beer_name_entry = tk.Entry(master = frame_top_left, width = 30)
    
    # Beer style dropdown list
    style_label = tk.Label(master = frame_top_middle, text = "Beer Style", bg="gold", width = 40)
    style_list = get_style_list()
    current_style = tk.StringVar(master = frame_top_middle)
    current_style.set(style_list[0])
    style_dropdown = tk.OptionMenu(frame_top_middle, current_style, *style_list)
    
    # Beer rating entry
    beer_rating_label = tk.Label(master = frame_top_right, text = "Beer Rating (0.0 - 5.0)", bg="gold", width = 20)
    beer_rating_entry = tk.Entry(master = frame_top_right, width = 20)
    
    # Button to trigger style score creation for user entered beer
    classify_button = tk.Button(master = frame_top,
                                command = classify,
                                height = 1,
                                width = 8,
                                text = "Classify",
                                )
    
    # Create initial plot of distribution for all beers
    x_all_beer = np.linspace(all_beers[0]- 3*all_beers[1], all_beers[0] + 3*all_beers[1], 1000)
    all_beer_graph_figure = Figure(figsize=(6.5,3), dpi =100)
    beer_plot = all_beer_graph_figure.add_subplot(111)
    beer_plot.plot(x_all_beer, stats.norm.pdf(x_all_beer, all_beers[0], all_beers[1]))
    beer_plot.set_yticklabels([" ", " ", " ", " "])
    graph_canvas = FigureCanvasTkAgg(all_beer_graph_figure, master = frame_middle_upper)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack()
    
    # Create custom legend below chart (in_built legend flexibility with FigureCanvasTkAgg is poor)
    all_beers_line_canvas = tk.Canvas(master = frame_middle_lower, height = 1.5, width = 10, bg = 'blue')
    all_beers_line_canvas.create_line(0,10,0,0)
    all_beers_legend_label = tk.Label(master = frame_middle_lower, text = "All Beers Distribution", bg="white", width = 19, height = 2)
    style_line_canvas = tk.Canvas(master = frame_middle_lower, height = 1.5, width = 10, bg = 'orange')
    style_line_canvas.create_line(0,10,0,0)
    style_legend_label = tk.Label(master = frame_middle_lower, text = " Style Distribution", bg="white", width = 15, height = 2)
    beer_line_canvas = tk.Canvas(master = frame_middle_lower, height = 1.5, width = 10, bg = 'green')
    beer_line_canvas.create_line(0,10,0,0)
    beer_legend_label = tk.Label(master = frame_middle_lower, text = "Beer Rating", bg="white", width = 11, height = 2)
    
    # Style rating score that automatically updates upon classification
    style_rating_score_label = tk.Label(master = frame_bottom, text = "Beer Style Rating", bg="gold", width = 20)
    style_rating_string = tk.StringVar(master = frame_bottom)
    style_rating_string.set("")
    style_rating_label = tk.Label(master = frame_bottom, textvariable = style_rating_string, bg="white", width = 20, height = 2)
    left_fill = tk.Label(master = frame_bottom, text = "", bg="gold", width = 25, height = 2)
    right_fill = tk.Label(master = frame_bottom, text = "", bg="gold", width = 25, height = 2)
    
    # Pack widgets and frames
    beer_name_label.pack()
    beer_name_entry.pack()
    style_label.pack()
    style_dropdown.pack()
    beer_rating_label.pack()
    beer_rating_entry.pack()
    classify_button.pack(side = tk.BOTTOM, anchor = "se")
    left_fill.pack(side = tk.LEFT)
    style_rating_score_label.pack(side = tk.LEFT)
    style_rating_label.pack(side = tk.LEFT)    
    right_fill.pack(side = tk.LEFT)
    all_beers_line_canvas.pack(side = tk.LEFT)  
    all_beers_legend_label.pack(side = tk.LEFT)  
    style_line_canvas.pack(side = tk.LEFT)  
    style_legend_label.pack(side = tk.LEFT)  
    beer_line_canvas.pack(side = tk.LEFT)  
    beer_legend_label.pack(side = tk.LEFT)    
    frame_top_left.pack(side = tk.LEFT)
    frame_top_middle.pack(side = tk.LEFT)
    frame_top_right.pack(side = tk.LEFT)
    frame_middle_upper.pack()
    frame_middle_lower.pack()   
    frame_top.pack()
    frame_middle.pack()
    frame_bottom.pack()
    
    window.mainloop()
