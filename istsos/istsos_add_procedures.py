import requests
import json
import csv

service = 'meteogr'
url = 'http://127.0.0.1/istsos/wa/istsos/services/' + service + '/procedures'

# Read all the procedures (stations) from the stations.csv file
# and add them to istSOS
# http://istsos.org/en/latest/doc/ws_registersensor.html

# Read stations from csv
with open('../stations.csv', mode='r') as stations_file:
    stations_reader = csv.DictReader(stations_file)

    # Create a procedure for every station
    for station in stations_reader:
        station_name = station['station_name'][:25] # istSOS name limit to 25 chars
        
        procedure = {
            "system_id":f"{station_name}",
            "system":f"{station_name}",
            "description":f"Meteo station in {station['geodivision_name']}. ID: {station['station_id']}",
            "keywords": "weather, meteorological, meteo",
            "identification":[
                {
                    "name":"uniqueID",
                    "definition":"urn:ogc:def:identifier:OGC:uniqueID",
                    "value":f"urn:ogc:def:procedure:x-istsos:1.0:{station_name}"
                }
            ],
            "classification":[
                {
                    "name":"System Type",
                    "definition":"urn:ogc:def:classifier:x-istsos:1.0:systemType",
                    "value":"insitu-fixed-point"
                },
                {
                    "name":"Sensor Type",
                    "definition":"urn:ogc:def:classifier:x-istsos:1.0:sensorType",
                    "value":"Meteo Station"
                }
            ],
            "characteristics":"",
            "contacts":[],
            "documentation":[],
            "capabilities":[],
            "location":{
                "type":"Feature",
                "geometry":{
                    "type":"Point",
                    "coordinates":[f"{station['X']}",f"{station['Y']}",f"{station['Z']}"]
                },
                "crs":{
                    "type":"name",
                    "properties":{"name":"4326"}
                },
                "properties":{
                    "name":f"{station_name}"
                }
            },
            "interfaces":"",
            "inputs":[],
            "outputs":[
                {
                    "name":"Time",
                    "definition":"urn:ogc:def:parameter:x-istsos:1.0:time:iso8601",
                    "uom":"iso8601",
                    "description":"",
                    "constraint":{}
                },
                {
                    "name":"air-temperature",
                    "definition":"urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
                    "uom":"°C",
                    "description":"mean temperature",
                    "constraint":{
                        "role":"urn:ogc:def:classifiers:x-istsos:1.0:qualityIndex:check:reasonable",
                        "interval":["-40","60"]
                    }
                },
                {
                    "name":"air-rainfall",
                    "definition":"urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall",
                    "uom":"mm",
                    "description":"total rainfall",
                    "constraint":{
                        "role":"urn:ogc:def:classifiers:x-istsos:1.0:qualityIndex:check:reasonable",
                        "interval":["0","500"]
                    }
                },
                {
                    "name":"air-wind-velocity",
                    "definition":"urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity",
                    "uom":"km/h",
                    "description":"Average wind velocity",
                    "constraint":{}
                },
                {
                    "name":"air-wind-direction",
                    "definition":"urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:direction",
                    "uom":"\u00b0",
                    "description":"Dominating wind direction",
                    "constraint":{}
                }
            ],
            "history":[]
        }

        r = requests.post(url, data=json.dumps(procedure))
        
        # Error during insertion
        if not r.json()['success']:
            print("Error: ", station)
            #print(r.json())
