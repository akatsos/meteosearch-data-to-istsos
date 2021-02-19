import requests
import time
import csv
import portolan
from os import path


def _parse_line(line):
    """
    Parse a line from the txt file.
    """

    # Example (The values in parentheses are the ones we want)
    #        MEAN                                HEAT  COOL         AVG WIND                DOM
    #  DAY   TEMP   HIGH    TIME   LOW    TIME   DAYS  DAYS  RAIN    SPEED   HIGH   TIME    DIR
    #  (1)  (10.3)  11.6    0:10   9.1   18:30   8.1   0.0   (0.0)   (7.6)   35.4    2:30   (N)
    # For more information: http://meteosearch.meteo.gr/dataHelp.asp

    # Split lines by spaces, create list from values, remove empty values
    line_values = list(filter(None, line.split(' ')))

    # Convert cardinal directions (wind) to degrees
    try:
        wind_dir = portolan.middle(line_values[12])
    # Line contains no wind directions
    except KeyError:
        wind_dir = "null"
    # Line contains no information at all
    except IndexError:
        return line_values[0], "null", "null", "null", "null"

    # Day, Mean Temperature, Rain, Average Wind Speed, Wind Direction
    return line_values[0], line_values[1], line_values[8], line_values[9], wind_dir
    

def _get_daily_values(session, station_id, year, month, measurements_writer):
    """
    POSTs and parses daily data from the txt file in response
    """
    # Request URL to get the data
    url = 'http://meteosearch.meteo.gr/FormProc.asp'

    # POST request body
    req_body = {
        'stationID': station_id,
        'SelectYear': year,
        'SelectMonth': month
    }

    # Pages returning 404 will get skipped
    station_data = session.post(url, req_body).text

    # Separator Flag. Used for getting the data inside the --------- lines
    sep_flag = False

    # Iterate through each line
    for line in station_data.splitlines():
        # Stops reading when second separator is reached
        if sep_flag and '-----------' in line:
            break
        
        # Lines between the separators
        if sep_flag:
            day, mean_temp, rain, avg_wind_speed, wind_dir = _parse_line(line)

            # Write daily measurements in csv
            measurements_writer.writerow({
                                    'year':year, 'month': month, 'day': day, 'mean_temperature': mean_temp, 
                                    'rain': rain, 'average_wind_speed': avg_wind_speed, 'dominant_wind_direction': wind_dir
                                    })

        # Sets the first separator flag
        if '-----------' in line:
            sep_flag = True

# --- --- ---

# Create session
meteo_session = requests.Session()

# Configuration
years = [2020]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Read stations from provided csv (get_all_stations.py)
with open('stations.csv', mode='r') as stations_file:
    stations_reader = csv.DictReader(stations_file)

    for station in stations_reader:
        file_path = f"station_measurements/{station['station_id']}-{station['station_name']}.csv"
        
        if not path.exists(file_path):
            # Create a csv file for every station
            with open(file_path, mode='w') as station_file:
                fieldnames = ['year', 'month', 'day', 'mean_temperature', 'rain', 'average_wind_speed', 'dominant_wind_direction']
                measurements_writer = csv.DictWriter(station_file, fieldnames=fieldnames)
                measurements_writer.writeheader()
                
                for year in years:
                    for month in months:
                        _get_daily_values(meteo_session, station['station_id'], year, month, measurements_writer)

            # Wait 0.5 seconds after every 12 requests to avoid
            # causing stress on meteo's web server.
            # Can be ommited
            time.sleep(0.5)