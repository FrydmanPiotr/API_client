"""
Project title: IGMW API client application
Author: Piotr Frydman
"""

from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3 as db
import requests
import time
import csv

class imgwApiClient(tk.Tk):
    def __init__(self):
        super().__init__()
        current_date = time.strftime("%d_%m_%Y", time.localtime())
        self.title(f"IMGW Api Client  |  Date: {current_date}")
        self.geometry("500x310+500+250")
        self.resizable(False, False)
        self.table_name = f"imgw_{current_date}"
        self.create_main_window()

    def get_data(self):
        url = 'https://danepubliczne.imgw.pl/api/data/synop'
        try:
            respons = requests.get(url).json()
            conn = db.connect("imgw.sqlite")
            c = conn.cursor()

            querry = f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                (City TEXT,
                Temperature FLOAT,
                Pressure INTEGER,
                Wind_speed INTEGER,
                Rainfall_total INTEGER)'''
            c.execute(querry)

            c.execute(f"SELECT * FROM {self.table_name}")
            if not c.fetchall():
                querry = f'''INSERT INTO {self.table_name}
                    (City, Temperature, Pressure,
                    Wind_speed, Rainfall_total) VALUES (?, ?, ?, ?, ?)'''
                for station in response:
                    city = station['stacja']
                    temperature = station['temperatura']
                    pressure = station['cisnienie']
                    wind = station['predkosc_wiatru']
                    rainfall = station['suma_opadu']
                    c.execute(querry, (city, temperature, pressure, wind, rainfall))
                conn.commit()
                
        except:
            tk.messagebox.showerror("Error", "Connection with IMGW API failed")

    def display_records(self,table):
        conn = db.connect("imgw.sqlite")
        c = conn.cursor()
        
        querry = f"SELECT * FROM {self.table_name} order by City asc"
        c.execute(querry)
        for row in c.fetchall():
            table.insert("", tk.END, values=row)
        c.close()
        conn.close()

    def save_in_csv(self):
        conn = db.connect("imgw.sqlite")
        c = conn.cursor()
        filename = self.table_name + ".csv"
        columns = ('City', 'Temperature', 'Pressure', 'Wind_speed', 'Rainfall_total')
        try:
            c.execute(f'SELECT * FROM {self.table_name} order by City asc')
            with open(filename, 'w', newline="") as file:
                csvwriter = csv.writer(file, delimiter=";")
                csvwriter.writerow(columns)
            
                for row in c.fetchall():
                    row = [str(val).replace('.', ',') if isinstance(val, float)
                           else val for val in row]
                    csvwriter.writerow(row)
                tk.messagebox.showinfo("Saving in CSV", "File created")
        except Exception as e :
            tk.messagebox.showerror("Error", f"{e}")
            
    def create_main_window(self):    
        columns = ('City', 'Temperature', 'Pressure', 'Wind_speed',
                   'Rainfall_total')
        table = ttk.Treeview(self, height=8, columns=columns, show='headings')
        for column in columns:
            table.column(column, stretch=False, width=90)
            table.heading(column, text=column)
        table.place(x=23, y=15)
        
        export = tk.Button(self, text="Export", width=6, bd=3, bg="#FFE5CC",
                           command=self.save_in_csv)
        export.place(x=180, y=210)
        update = tk.Button(self, text="Update", width=6, bd=3, bg="#FFE5CC",
                           command=self.get_data)
        update.place(x=250, y=210)
        #show records
        self.display_records(table)
            
try:
    iac = imgwApiClient()
    iac.mainloop()
except Exception as e:
    tk.messagebox.showerror("Error", f"{e}") 
