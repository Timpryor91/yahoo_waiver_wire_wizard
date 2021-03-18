# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import tkinter as tk
from classes.interface_class import Interface

if __name__ == "__main__":
    
    # Initiate tool interface
    window = tk.Tk()
    tool_interface = Interface(window)
    window.mainloop()