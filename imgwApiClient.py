"""
Project title: IGMW API client application
Author: Piotr Frydman
"""
import requests
import json
import csv
import sqlite3
import time
from plotly.graph_objs import Bar
from plotly import offline

# make an API call and process the response
url = 'https://danepubliczne.imgw.pl/api/data/synop'
response = requests.get(url)
if response.status_code != requests.codes.ok:
    print("Błąd połączenia z API")
    exit()

response_dict = response.json()

# Create a table name without special characters
current_date = time.strftime("%d_%m_%Y", time.localtime())
table_name = f"IMGW_{current_date}"
filename = f"imgw_{current_date}.csv"

conn = sqlite3.connect('imgw.sqlite')
c = conn.cursor()

# creating table
c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
        (stacja TEXT,
        temperatura FLOAT,
        ciśnienie INTEGER,
        wiatr INTEGER,
        opady INTEGER)''')

c.execute(f"delete from {table_name}")

for station in response_dict:
    stacja = station['stacja']
    temperatura = station['temperatura']
    cisnienie = station['cisnienie']
    wiatr = station['predkosc_wiatru']
    opady = station['suma_opadu']

    c.execute(f"INSERT INTO {table_name} (stacja, temperatura, ciśnienie,wiatr,opady) VALUES (?, ?, ?,?,?)",
              (stacja, temperatura, cisnienie,wiatr,opady))
      
#saving changes and close connection
conn.commit()
conn.close()

conn = sqlite3.connect('imgw.sqlite')
c = conn.cursor()
for db in c.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"):
    print(db)

#saving data from response to file
with open(filename, 'w',newline="") as file:
    csvwriter=csv.writer(file, delimiter=";")
    headers=['Lokalizacja','Temperatura','Ciśnienie','Wiatr','Opady']
    csvwriter.writerow(headers)

    #display columns names
    querry = c.execute(f'SELECT * FROM {table_name}')
    for data in querry:
        print(data)
        csvwriter.writerow(data)
file.close()


c.close()
