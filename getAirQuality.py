#--------------------------------------------------------
#Grabs data from purpleair.com and stores it in an InfluxDB
#
#--------------------------------------------------------
from operator import contains
import requests
import json
import os
import argparse
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


#pull data from config file
parser = argparse.ArgumentParser(description='Gimme')
parser.add_argument('-s', '--influxdbhost', required=True, help='Influxdb host')
parser.add_argument('-P', '--influxdbport', default=8086, help='Influxdb port')
parser.add_argument('-u', '--influxdbusername', required=True, help='Influxdb username')
parser.add_argument('-p', '--influxdbpass', required=True, help='Influxdb pass')
parser.add_argument('-d', '--influxdbdatabase', default="airquality", help='Influxdb database name')
parser.add_argument('-i', '--ids', required=True, help='PurpleAir.com IDs')
parser.add_argument('-k', '--key', required=True, help='PurpleAir.com API Key')
args = parser.parse_args()

key=args.key

#--------------------------------------------------------
#Get weather information from openweather
#--------------------------------------------------------
ids = args.ids
id_arry=ids.split()

for id in id_arry:
    print("Getting id " + id)

    url = "https://api.purpleair.com/v1/sensors/"+id
    headers = { 'X-API-Key' : key}
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)

    #remove all stats nodes b/c it was causing problems
    temp_data=[]
    for data in json_data["sensor"]:
        print(data)
        if "stats" in data:
            temp_data.append(data)
    for remove in temp_data:
        del json_data["sensor"][remove]

    #--------------------------------------------------------
    #post data to influxdb
    #--------------------------------------------------------
    json_body = [
        {
            "measurement": "main",
            "tags": {
                "id": id,
                #"timezone":json_data["timezone"],
                "label":json_data["sensor"]["name"]
            },
            "fields": json_data["sensor"]
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




