#--------------------------------------------------------
#Grabs data from openweather.org and stores it in an InfluxDB
#
#--------------------------------------------------------
from operator import contains
import requests
import json
import os
import argparse
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import urllib
import requests

#pull data from config file
parser = argparse.ArgumentParser(description='Gimme')
parser.add_argument('-s', '--influxdbhost', required=True, help='Influxdb host')
parser.add_argument('-P', '--influxdbport', default=8086, help='Influxdb port')
parser.add_argument('-u', '--influxdbusername', required=True, help='Influxdb username')
parser.add_argument('-p', '--influxdbpass', required=True, help='Influxdb pass')
parser.add_argument('-d', '--influxdbdatabase', default="airquality", help='Influxdb database name')
parser.add_argument('-z', '--zip', required=True, help='Zipcode')
parser.add_argument('-k', '--key', required=True, help='OpenWeather.org API Key')
args = parser.parse_args()

key=args.key
zip = args.zip
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(zip) +'?format=json'
adress_data = requests.get(url).json()

print("Getting zipcode " + zip)
url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=' + adress_data[0]["lat"] + '&lon=' + adress_data[0]["lon"] + '&appid=' + key
json_data = requests.get(url).json()

#--------------------------------------------------------
#post data to influxdb
#--------------------------------------------------------
json_body = [
    {
        "measurement": "main",
        "tags": {
            "id": zip,
            #"timezone":json_data["timezone"],
            #"label": json_data["list"][0]['components']
        },
        "fields": json_data["list"][0]['components']
    }
]

client = InfluxDBClient(host=args.influxdbhost, port=args.influxdbport, username=args.influxdbusername, password=args.influxdbpass,database=args.influxdbdatabase)

try:
        response = client.write_points(json_body)
        print("InfluxDB client response: ", response)
        print("JSON sent: ", json_body)
        exit(0)
        
except InfluxDBClientError as e:
        print("Influxdb Error: ", e.content)




