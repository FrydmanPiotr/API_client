"""
Project title: IGMW API client application (GUI)
Author: Piotr Frydman
"""

import tkinter as tk
from tkinter import ttk

class imgwApiGui:
    def __init__(self, main):
        main.title("IMGW Api Client")
        main.geometry("500x280+500+250")
        main.resizable(False, False)
        self.create_widgets(main)

    def create_widgets(self,main):
        #shows records
        columns=('City','Temperature', 'Pressure','Wind speed','Rainfall total')
        table = ttk.Treeview(main,height=8,columns=columns,show='headings')
        for column in table["columns"]:
            table.column(column, stretch=False, width=90)
            table.heading(column,text=column)
        table.place(x=23,y=15)
        
        tk.Label(main, text="Date").place(x=20,y=220)
        ttk.Combobox(main, state="readonly").place(x=53,y=220)
        
        tk.Label(main, text="Hour").place(x=210,y=220)
        ttk.Combobox(main, state="readonly").place(x=250,y=220)
        btn=tk.Button(main, text="Show",width=6,height=2,bd=3,bg="#FFE5CC")
        btn.place(x=410, y=210)
        
root = tk.Tk()
imgwApiGui(root)
root.mainloop()
