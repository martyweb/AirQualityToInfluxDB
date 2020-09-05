#--------------------------------------------------------
#Grabs data from purpleair.com and stores it in an InfluxDB
#
#--------------------------------------------------------
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
args = parser.parse_args()

#--------------------------------------------------------
#Get weather information from openweather
#--------------------------------------------------------
ids = args.ids
id_arry=ids.split()

for id in id_arry:
    print("Getting id " + id)

    url = "https://www.purpleair.com/json?show="+id
    response = requests.request("GET", url)
    json_data = json.loads(response.text)

    print("Got this data back:")
    print(json_data["results"][0])

    #--------------------------------------------------------
    #post data to influxdb
    #--------------------------------------------------------
    json_body = [
        {
            "measurement": "main",
            "tags": {
                "id": id,
                #"timezone":json_data["timezone"],
                "label":json_data["results"][0]["Label"]
            },
            "fields": json_data["results"][0]
        }
    ]

    client = InfluxDBClient(host=args.influxdbhost, port=args.influxdbport, username=args.influxdbusername, password=args.influxdbpass,database=args.influxdbdatabase)

    try:
            response = client.write_points(json_body)
            print("InfluxDB client response: ", response)
            print("JSON sent: ", json_body)
            exit(0)
            
    except InfluxDBClientError as e:
            print(e.content)




