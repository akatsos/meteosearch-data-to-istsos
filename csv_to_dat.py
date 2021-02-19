import csv
import os
from datetime import datetime

def _get_datetime_for_file(msm_list):
    """
    Get the datetime of the last observation that contains no null measurements
    """
    # Get last measurement date
    msm_list.reverse()
    for msm in msm_list:
        # Skip any line that contains a null value
        if 'null' not in msm.values():
            datetime_title = datetime(int(msm['year']), int(msm['month']), int(msm['day']), 0, 0, 0, 0).strftime('%Y%m%d%H%M%S%f')[:-4]
            
            return datetime_title

# --- --- --- ---

folder_source = 'station_measurements/'
folder_dest = 'stations_dat/'

# For every file in source folder
for station_file in os.listdir(folder_source):
    station_name = station_file.split('-')[1][:-4][:25]

    with open(folder_source + station_file, mode='r') as csv_file:
        stations_reader = csv.DictReader(csv_file)
        msm_list = list(stations_reader)

        # Get datetime for .dat title
        dt_title = _get_datetime_for_file(msm_list)
        msm_list.reverse()

        with open(folder_dest + f"{station_name}_{dt_title}.dat", mode='w') as dat_file:
            fieldnames = [
                        'urn:ogc:def:parameter:x-istsos:1.0:time:iso8601',
                        'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature',
                        'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall',
                        'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity',
                        'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:direction'
                        ]

            writer = csv.DictWriter(dat_file, fieldnames=fieldnames)
            writer.writeheader()
            
            # For each measurement in a file
            for msm in msm_list:
                # Skip any line that contains a null value
                if 'null' not in msm.values():
                    try:
                        datetime_iso = datetime(int(msm['year']), int(msm['month']), int(msm['day']), 0, 0, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f') + '+0000'
                    # Skip lines with wrong date format
                    except ValueError:
                        continue

                    writer.writerow({
                            'urn:ogc:def:parameter:x-istsos:1.0:time:iso8601': datetime_iso,
                            'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature': msm['mean_temperature'],
                            'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall': msm['rain'],
                            'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity': msm['average_wind_speed'],
                            'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:direction': msm['dominant_wind_direction']
                            })