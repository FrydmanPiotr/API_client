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

class ImgwApiClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.date=time.strftime('%d_%m_%Y', time.localtime())
        self.table_name = f"imgw_{self.date}"
        self.conn = db.connect("imgw.sqlite")
        self.cur = self.conn.cursor()
        self.setup_ui()
        self.load_menu()      

    def setup_ui(self):
        self.title(f"IMGW Api Client  |  Date: {self.date}")
        self.geometry("500x310+500+250")
        self.resizable(False, False)
    
    def get_data(self,table): 
        try:
            url = 'https://danepubliczne.imgw.pl/api/data/synop'
            response = requests.get(url).json()            
            query = f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                (City TEXT, Temperature FLOAT,
                Pressure INTEGER, Wind_speed INTEGER,
                Rainfall_total INTEGER)'''
            self.cur.execute(query)

            self.cur.execute(f"SELECT * FROM {self.table_name}")
            if not self.cur.fetchall():
                query = f'''INSERT INTO {self.table_name}
                    (City, Temperature, Pressure,
                    Wind_speed, Rainfall_total) VALUES (?, ?, ?, ?, ?)'''
                for station in response:
                    city = station['stacja']
                    temperature = station['temperatura']
                    pressure = station['cisnienie']
                    wind = station['predkosc_wiatru']
                    rainfall = station['suma_opadu']
                    self.cur.execute(query, (city, temperature, pressure, wind,
                                      rainfall))
                self.conn.commit()
            self.display_data(table)
        except Exception as e:
            tk.messagebox.showerror("Error", f"{e}")

    def display_data(self,table):
        query = f"SELECT * FROM {self.table_name} order by City asc"
        self.cur.execute(query)
            
        for row in self.cur.fetchall():
            table.insert("", tk.END, values=row)
        self.cur.close()
        self.conn.close()

    def export_csv(self,columns):
        file = f'{self.table_name}.csv'
        try:
            query = f'SELECT * FROM {self.table_name} order by City asc'
            self.cur.execute(query)
            with open(file, 'w', newline="") as f:
                csvwriter = csv.writer(f, delimiter=";")
                csvwriter.writerow(columns)
            
                for row in self.cur.fetchall():
                    row = [str(val).replace('.', ',') if isinstance(val, float)
                           else val for val in row]
                    csvwriter.writerow(row)
                tk.messagebox.showinfo("Saving in CSV", "File created")
        except Exception as e :
            tk.messagebox.showerror("Error", f"{e}")
            
    def load_menu(self):
        columns = ('City', 'Temperature', 'Pressure', 'Wind_speed',
                   'Rainfall_total')
        table = ttk.Treeview(self, height=8, columns=columns, show='headings')
        for column in columns:
            table.column(column, stretch=False, width=90)
            table.heading(column, text=column)
        table.place(x=23, y=15)
        
        tk.Button(self, text="Export", width=6, bd=3, bg="#FFE5CC",
                command=lambda: self.export_csv(columns)).place(x=180, y=210)
        tk.Button(self, text="Load", width=6, bd=3, bg="#FFE5CC",
                  command=lambda: self.get_data(table)).place(x=250, y=210)
            
iac = ImgwApiClient()
iac.mainloop()    
