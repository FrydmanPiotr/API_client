## API client application

## Table of contents
* Description
* Technologies
* Setup
* Sources

## Description 
Simple client app for IMGW API

Legend:
+ Load - connection to server 
and setting data in the database
+ Search - displaying data based on date
+ Export - exporting data to a CSV file

![ImgwAPiClient GUI](https://github.com/FrydmanPiotr/ImgwApiClient/blob/main/images/imgw_api_client.png)

## Technologies 
Project is created with:
* Python 3.11

## Setup
To run this project, install locally following Python modules:
* requests

To install this package write following
command in system terminal:

```
$ pip install requests
```

__Important: requires prior installation of PIP 
(Python package manager). You can do this by
running these commands in the terminal:__

```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
```

## Sources
API is available at: [IMGW API](https://danepubliczne.imgw.pl/api/data/synop)

__IMGW announcement: "Using the Service means that the User agrees to
comply with the provisions of the Regulations, therefore each User is
obliged to read the Regulations before starting to
use the Service"__ [Regulations](https://danepubliczne.imgw.pl/regulations)
