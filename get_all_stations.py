import requests
from bs4 import BeautifulSoup
import ast
import csv
import json
from unidecode import unidecode
from dms2dec.dms_convert import dms2dec

def _get_XYZ(session, station_id):
    """
    POSTs and parses XYZ coordinates
    """
    # Request URL to get the data
    url = 'http://meteosearch.meteo.gr/FormProc.asp'

    # POST request body
    req_body = {
        'stationID': station_id,
        'SelectYear': 2020,
        'SelectMonth': 12
    }
    response = session.post(url, req_body)

    # Check for code 2xx.
    if response.ok:
        station_data = response.text

        xyz_line = station_data.splitlines()[3]
        # Check if the 3rd line contains the data.
        # Sometimes the 2nd one does.
        if 'LAT:' in xyz_line:
            z = xyz_line.split('ELEV:')[1].split('m')[0].strip()              
            x_dms = xyz_line.split('LONG:')[1].split('E')[0].strip()
            y_dms = xyz_line.split('LAT:')[1].split('N')[0].strip()
            # Check if line contains coordinates  
            if x_dms and y_dms:
                # Convert DMS to DD
                x = dms2dec(x_dms + "E")
                y = dms2dec(y_dms + "N")

                return x, y, z
        else:
            xyz_line = station_data.splitlines()[2]
            if 'LAT:' in xyz_line:
                z = xyz_line.split('ELEV:')[1].split('m')[0].strip()           
                x_dms = xyz_line.split('LONG:')[1].strip()
                y_dms = xyz_line.split('LAT:')[1].split('LONG')[0].strip()
                # Check if line contains coordinates
                if x_dms and y_dms:
                    x = dms2dec(x_dms.replace("deg", "°").replace("min", "'") + " 00'\"E")
                    y = dms2dec(y_dms.replace("deg", "°").replace("min", "'") + "00'\"N")
                    
                    return x, y, z
    # If no data is found
    return None, None, None

url = 'http://meteosearch.meteo.gr/'

# Gets the response as text
response = requests.get(url).text

# Gets the script div containing the station info as string
script_div = str(BeautifulSoup(response, 'html.parser').find('script', src='', type=''))

# Remove undesired info
stations_list = script_div.split('top.jsRawData_Recordset2 = ')[1].split('\ntop.Recordset2')[0].replace('\n', '')

# Evaluate expression nodes
stations_list = ast.literal_eval(stations_list)

# Load extras
with open("extras.json") as extras_file:
    data = json.load(extras_file)
    geodivisions = data['geodivisions']

# Create session
meteo_session = requests.Session()

# Start writing to csv file
with open('stations.csv', mode='w') as csv_file:
    fieldnames = ['station_id', 'station_name', 'geodivision_id', 'geodivision_name', 'X', 'Y', 'Z']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for station in stations_list:
        # Remove empty stations and stations not in Greece
        if station and ('' not in station) and ('StationsID' not in station) and (station[1] != '21'):
            x, y, z = _get_XYZ(meteo_session, station[0])
            # Remove unsupported characters and replace greek characters
            station_name_en = unidecode(station[2]).replace("-", " ").replace("(", "").replace(")", "").replace("/", " ").replace(" ", "_").replace("__", "_").replace("__", "_")

            # If coordinates were provided
            if x and y and z:
                writer.writerow({
                    'station_id': station[0], 
                    'station_name': station_name_en, 
                    'geodivision_id': station[1], 
                    'geodivision_name': geodivisions[station[1]],
                    'X': x, 'Y': y, 'Z': z
                    })
