"""
Project title: API client application
Author: Piotr Frydman
"""

import requests
import json
import csv
import sqlite3 as db
import time
from plotly.graph_objs import Bar
from plotly import offline

current_date = time.strftime("%d_%m_%Y", time.localtime())
table_name = f"imgw_{current_date}"
filename = table_name + ".csv"

def api_request():
    #make an API call and process the response
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    try:
        response = requests.get(url)
        response_dict = response.json()
        save_data_in_db(response_dict)
    except Exception as e:
        print("Error:", e)

def connect_db():
    db_name = "imgw.sqlite"
    conn = db.connect(db_name)
    return conn

def save_data_in_db(response_dict):
    #connect to database
    conn = connect_db()
    c = conn.cursor()

    #creating table
    querry = f'''CREATE TABLE IF NOT EXISTS {table_name}
            (stacja TEXT,
            temperatura FLOAT,
            ciśnienie INTEGER,
            wiatr INTEGER,
            opady INTEGER)'''
    c.execute(querry)

    #clear existing data 
    querry = f"DELETE FROM {table_name}"
    c.execute(querry)

    #inserting data
    for station in response_dict:
        stacja = station['stacja']
        temperatura = station['temperatura']
        cisnienie = station['cisnienie']
        wiatr = station['predkosc_wiatru']
        opady = station['suma_opadu']

        querry = f'''INSERT INTO {table_name} (stacja, temperatura, ciśnienie, wiatr, opady)
            VALUES (?, ?, ?, ?, ?)'''
        c.execute(querry, (stacja, temperatura, cisnienie, wiatr, opady))

    conn.commit()
    conn.close()

def save_data_in_csv():
    #connect to database
    conn = connect_db()
    c = conn.cursor()

    #saving data from database to CSV file
    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file, delimiter=";")
        headers = ['Lokalizacja', 'Temperatura', 'Ciśnienie', 'Wiatr', 'Opady']
        csvwriter.writerow(headers)

        #writing data from database to CSV
        querry = f'SELECT * FROM {table_name}'
        c.execute(querry)
        for row in c.fetchall():
            row = [str(val).replace('.', ',') if isinstance(val, float) else val for val in row]
            csvwriter.writerow(row)
    conn.close()

def create_visualisation():
    #connect to database
    conn = connect_db()
    c = conn.cursor()

    #fetching data from the database
    querry = f'SELECT stacja, temperatura FROM {table_name} ORDER BY temperatura ASC'
    station, parameter = [], []

    c.execute(querry)
    for stacja, temperatura in c.fetchall():
        station.append(stacja)
        parameter.append(temperatura)

    #creating visualization
    data = [{
        'type': 'bar',
        'x': station,
        'y': parameter,
        'marker': {
            'color': 'rgb(180,20,20)',
            'line': {'width': 1.5, 'color': 'rgb(50,25,25)'}
        },
        'opacity': 0.6,
    }]
    layout = {
        'title': f'Temperatura we wszystkich stacjach IMGW ({current_date})',
        'titlefont': {'size': 28},
        'xaxis': {
            'title': 'Temperatura (*C)',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
        'yaxis': {
            'title': 'Lokalizacja stacji',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
    }
    fig = {'data': data, 'layout': layout}
    offline.plot(fig, filename='temperature_imgw.html')
    conn.close()

try:
    api_request()
    save_data_in_csv()
    create_visualisation()
except Exception as e:
    print("Error:", e)
