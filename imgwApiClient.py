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
        self.current_date=time.strftime('%d_%m_%Y', time.localtime())
        self.table_name = f"imgw_{self.current_date}"
        self.conn = db.connect("imgw.sqlite")
        self.cur = self.conn.cursor()             

    def connect_to_database(self):
        self.conn = db.connect("imgw.sqlite")
        self.cur = self.conn.cursor()

    def close_database_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
                
    def create_table(self):
        query = f'''CREATE TABLE IF NOT EXISTS {self.table_name}
            (City TEXT,
            Temperature FLOAT,
            Pressure INTEGER,
            Wind_speed INTEGER,
            Rainfall_total INTEGER)'''
        self.cur.execute(query)
    
    def fetch_data(self, date):
        url = 'https://danepubliczne.imgw.pl/api/data/synop'
        self.connect_to_database()
        self.create_table()
        try:
            response = requests.get(url).json()
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
                    self.cur.execute(query, (city, temperature, pressure, wind, rainfall))
            self.conn.commit()
            
            #adding new date to combobox
            date['values'] = self.show_dates()
            
            tk.messagebox.showinfo("Info","Database is up to date")
        except requests.exceptions.RequestException:
            tk.messagebox.showerror("Error", "Failed to connect to IMGW API.\n"\
                    "Please, check your network connection.")
        finally:
            self.close_database_connection()
            
    def setup_ui(self):
        self.title(f"IMGW Api Client")
        self.geometry("500x270+500+250")
        self.resizable(False, False)
        self.load_menu()

    def load_menu(self):
        columns = ('City', 'Temperature', 'Pressure', 'Wind_speed',
                   'Rainfall_total')
        table = ttk.Treeview(self, height=8, columns=columns, show='headings')
        for column in columns:
            table.column(column, stretch=False, width=90)
            table.heading(column, text=column)
        table.place(x=23, y=15)

        tk.Button(self, text="Export", width=6, bd=3, bg="#FFE5CC",
            command=lambda: self.export_csv(columns,date)).place(x=315, y=210)
        
        tk.Button(self, text="Load", width=6, bd=3, bg="#FFE5CC",
            command=lambda: self.fetch_data(date)).place(x=380, y=210)

        tk.Label(self, text="Date").place(x=60, y=217)
        date = ttk.Combobox(self, values=self.show_dates(), state="readonly")
        date.place(x=100, y=217)
        
        btn = tk.Button(self, text="Search", width=6, bd=3, bg="#FFE5CC",
                        command=lambda: self.display_data(table, date))
        btn.place(x=250, y=210)

    def display_data(self,table,date):
        selected_date = date.get()
        self.connect_to_database()
        try:
            query = f"SELECT * FROM imgw_{selected_date} order by City asc"
            self.cur.execute(query)

            #clear and insert new contents 
            table.delete(*table.get_children())    
            for row in self.cur.fetchall():
                table.insert("", tk.END, values=row)
                
        except Exception:
            tk.messagebox.showinfo("Info", "Select date")
        finally:
            self.close_database_connection()

    def show_dates(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cur.execute(query)
        dates = [i[0][5:15] for i in self.cur.fetchall()]
        return dates
        
    def export_csv(self,columns,date):
        selected_date = date.get()
        self.connect_to_database()
        file = f'imgw_{selected_date}.csv'  
        try:
            query = f'SELECT * FROM imgw_{selected_date} order by City asc'
            self.cur.execute(query)
            with open(file, 'w', newline="") as f:
                csvwriter = csv.writer(f, delimiter=";")
                csvwriter.writerow(columns)
            
                for row in self.cur.fetchall():
                    row = [str(val).replace('.', ',') if isinstance(val, float)
                           else val for val in row]
                    csvwriter.writerow(row)
                tk.messagebox.showinfo("Saving in CSV", "File created")

        except Exception:
            tk.messagebox.showinfo("Info", "Select date")
        finally:
            self.close_database_connection()
            
iac = ImgwApiClient()
iac.setup_ui()
iac.mainloop()
