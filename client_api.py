"""
Project title: API client application
Author: Piotr Frydman
"""
import requests
import json
import csv

#make an API call and process the response
url = 'https://danepubliczne.imgw.pl/api/data/synop'
response = requests.get(url)
if response.status_code != requests.codes.ok:
    print("Błąd połączenia z API")

else:
    #create file 
    response_dict = response.json()
    with open("dane_imgw.csv", 'w',newline="") as file:
        csvwriter=csv.writer(file, delimiter=";")
        headers=['Lokalizacja','Temperatura','Ciśnienie','Wiatr','Opady']
        csvwriter.writerow(headers)
    file.close()

    #saving data from response to file
    with open("dane_imgw.csv", 'a',newline="") as file:
        csvwriter=csv.writer(file, delimiter=";")
        data = []
        for station in response_dict:
            data.append(station['stacja'])
            #replace - swapping signs to correct format insert in Excel
            data.append(station['temperatura'].replace(".", ","))
            data.append(station['cisnienie'])
            data.append(station['predkosc_wiatru'])
            data.append(station['suma_opadu'].replace(".", ","))
            csvwriter.writerow(data)
            data.clear()
    file.close()
