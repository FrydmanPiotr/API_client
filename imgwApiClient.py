"""
Project title: IGMW API client application
Author: Piotr Frydman
"""

import tkinter as tk
from tkinter import ttk,messagebox
import requests
import csv
import sqlite3 as db
import time

current_date = time.strftime("%d_%m_%Y", time.localtime())
table_name = f"imgw_{current_date}"

def get_data():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    try:
        response = requests.get(url).json()
        conn = db.connect("imgw.sqlite")
        c = conn.cursor()

        querry = f'''CREATE TABLE IF NOT EXISTS {table_name}
            (City TEXT,
            Temperature FLOAT,
            Pressure INTEGER,
            Wind_speed INTEGER,
            Rainfall_total INTEGER)'''
        c.execute(querry)

        c.execute(f"SELECT * FROM {table_name}")
        if not c.fetchall():
            querry = f'''INSERT INTO {table_name} (City, Temperature, Pressure,
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

def display_records(table):
    conn = db.connect("imgw.sqlite")
    c = conn.cursor()
    
    querry = f"SELECT * FROM {table_name} order by City asc"
    c.execute(querry)
    for row in c.fetchall():
        table.insert("", tk.END, values=row)
    c.close()
    conn.close()

def save_in_csv():
    conn = db.connect("imgw.sqlite")
    c = conn.cursor()
    filename = table_name + ".csv"
    columns = ('City', 'Temperature', 'Pressure', 'Wind_speed', 'Rainfall_total')
    try:
        c.execute(f'SELECT * FROM {table_name} order by City asc')
        with open(filename, 'w', newline="") as file:
            csvwriter = csv.writer(file, delimiter=";")
            csvwriter.writerow(columns)
        
            for row in c.fetchall():
                row = [str(val).replace('.', ',') if isinstance(val, float)
                       else val for val in row]
                csvwriter.writerow(row)
            tk.messagebox.showinfo("Saving in CSV", "File was created")
    except Exception as e :
        tk.messagebox.showerror("Error", f"{e}")
        
def create_main_window():
    root.title(f"IMGW Api Client  |  {current_date}")
    root.geometry("500x310+500+250")
    root.resizable(False, False)
    
    columns = ('City', 'Temperature', 'Pressure', 'Wind_speed',
               'Rainfall_total')
    table = ttk.Treeview(root, height=8, columns=columns, show='headings')
    for column in columns:
        table.column(column, stretch=False, width=90)
        table.heading(column, text=column)
    table.place(x=23, y=15)
    
    export = tk.Button(root, text="Export", width=6, bd=3, bg="#FFE5CC",
                       command=save_in_csv)
    export.place(x=180, y=210)
    #connect with api
    get_data()
    display_records(table)
        
try:
    root = tk.Tk()
    create_main_window()
except Exception as e:
    tk.messagebox.showerror("Error", f"{e}")

root.mainloop()

    

