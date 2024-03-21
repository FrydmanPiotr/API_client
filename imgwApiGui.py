"""
Project title: IGMW API client application (GUI)
Author: Piotr Frydman
"""

import tkinter as tk
from tkinter import ttk

class imgwApiGui:
    def __init__(self, main):
        frame = tk.Frame(main)
        frame.pack()
        main.title("IMGW Api Client")
        main.geometry("600x300+500+250")
        main.resizable(False, False)
        
        #grid of elments
        frame.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=2)
        main.rowconfigure(0, weight=3)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)
        self.create_widgets(frame)

    def create_widgets(self, frame):
        #shows records
        self.table = ttk.Treeview(frame)
        self.table.grid(row=0,column=0)
        
        self.date_label = tk.Label(frame, text="Date")
        self.date_label.grid(row=1, column=0)
        self.date_combo = ttk.Combobox(frame, state="readonly")
        self.date_combo.grid(row=1, column=1)
        
        self.hour_label = tk.Label(frame, text="Hour")
        self.hour_label.grid(row=2, column=0)
        self.hour_combo = ttk.Combobox(frame, state="readonly")
        self.hour_combo.grid(row=2, column=1)
        
        self.select_button = tk.Button(frame, text="Show", pady=5, padx=5)
        self.select_button.grid(row=2, column=2)
        
root = tk.Tk()
imgwApiGui(root)
root.mainloop()
