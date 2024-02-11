"""
Nazwa: Aplikacja klient API
Autor: Piotr Frydman
"""
import requests
import json
import csv

#Wykonanie wywołania API i przetworzenie odpowiedzi.
url = 'https://danepubliczne.imgw.pl/api/data/synop'
response = requests.get(url)
if response.status_code != requests.codes.ok:
    print("Błąd połączenia z API")

else:
    #utworzenie pliku 
    response_dict = response.json()
    with open("dane_imgw.csv", 'w',newline="") as file:
        csvwriter=csv.writer(file, delimiter=";")
        headers=['Lokalizacja','Temperatura','Ciśnienie','Wiatr','Opady']
        csvwriter.writerow(headers)
    file.close()

    #zapisanie danych z odpowiedzi do pliku
    with open("dane_imgw.csv", 'a',newline="") as file:
        csvwriter=csv.writer(file, delimiter=";")
        data = []
        for station in response_dict:
            data.append(station['stacja'])
            #replace - zamiana znaków dla poprawnego formatowania Excel
            data.append(station['temperatura'].replace(".", ","))
            data.append(station['cisnienie'])
            data.append(station['predkosc_wiatru'])
            data.append(station['suma_opadu'].replace(".", ","))
            csvwriter.writerow(data)
            data.clear()
    file.close()
