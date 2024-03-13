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
try:
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print("Error")
    response_dict = response.json()
    
    # Create a table name without special characters
    current_date = time.strftime("%d_%m_%Y", time.localtime())
    table_name = f"IMGW_{current_date}"
    filename = f"imgw_{current_date}.csv"
    db_name = "imgw.sqlite"

    conn = sqlite3.connect(db_name)
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

    conn = sqlite3.connect(db_name)
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

    querry = c.execute(f'SELECT stacja, temperatura FROM {table_name} order by temperatura asc')

    station, parameter = [], []

    for stacja,temperatura in querry:
        station.append(stacja)
        parameter.append(temperatura)

    #creating visualisation
    data = [{
        'type':'bar',
        'x': station,
        'y': parameter,
        'marker':{
            'color':'rgb(180,20,20)',
            'line':{'width':1.5,'color': 'rgb(50,25,25)'}
            },
        'opacity':0.6,
        }]
    layout={
        'title': f'Temperatura we wszystkich stacjach IMGW ({current_date})',
        'titlefont': {'size':28},
        'xaxis': {
            'title':'Temperatura (*C)',
            'titlefont':{'size':24},
            'tickfont':{'size':14},
            },
        'yaxis': {
            'title': 'Lokalizacja stacji',
            'titlefont':{'size':24},
            'tickfont':{'size':14},
            },
        }
    fig={'data':data,'layout': layout}
    offline.plot(fig, filename='temperature_imgw.html')
       
    c.close()

except:
    print("Error: Failed to connect with IMGW API")
