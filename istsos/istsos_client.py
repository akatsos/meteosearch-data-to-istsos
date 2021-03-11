import requests
import json
import csv
import os

def getProcedures(host, service):
    """
    Get all the procedures (stations) using the WA-REST API
    """

    proc_url = f"http://{host}/istsos/wa/istsos/services/{service}/procedures/operations/getlist"

    # Request and Get the procedures from the response
    procedures = json.loads(requests.get(proc_url).text)['data']

    return procedures


def getObservationValues(host, service, offering, procedure, dateFrom, dateTo):
    """
    Get observations using the SOS 1.0.0 API
    """

    url = (f"http://{host}/istsos/{service}?service=SOS&version=1.0.0"
        f"&request=GetObservation&offering={offering}"
        f"&procedure=urn:ogc:def:procedure:x-istsos:1.0:{procedure}"
        "&observedProperty=urn:ogc:def:parameter:x-istsos:1.0:meteo"
        f"&eventTime={dateFrom}/{dateTo}"
        "&responseFormat=application/json")

    # Request Get the values from the response
    observation = json.loads(requests.get(url).text)['ObservationCollection']['member'][0]['result']['DataArray']['values']

    return observation


def printObservationValues(procedure_name, observation_values):
    """
    Just prints the observation values in an easy to read way
    """
    print(procedure_name)
    print("Date \t\t\t\t Temperature \t Rainfall \t Wind Speed \t Wind Direction")

    for value in observation_values:
        print(f"{value[0]} \t {value[1]} \t\t {value[2]} \t\t {value[3]} \t\t {value[4]}")


def saveToCSV(procedure_name, observation_values):
    """
    Save the observations in a CSV file.
    Each station gets saved in a different file
    """

    # Where our csv files will be saved
    folder_path = './istsos_observations/'

    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    with open(folder_path + f"{procedure_name}.csv", mode='w') as csv_file:
        fieldnames = ['Date', 'Temperature', 'Rainfall', 'Wind_Speed', 'Wind_Direction']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for value in observation_values:
            writer.writerow({
                'Date':value[0],
                'Temperature':value[1],
                'Rainfall':value[2],
                'Wind_Speed':value[3],
                'Wind_Direction':value[4]
            })

# --- Main ---

# Example
# Get the observations of all the procedures (stations) for June 2020

# Settings
host = 'localhost'
service = 'meteogr'
offering = 'temporary'

# Datetimes in ISO8601
dateFrom = '2020-06-01T00:00:00+0200'
dateTo = '2020-06-30T00:00:00+0000'

# List of procedures (stations)
# Manually enter the stations that you wish to get the observations from
procedures = []

# Get all the available procedures
procedures = getProcedures(host, service)

for procedure in procedures:

    # Get observations for the procedure
    observation_values = getObservationValues(host, service, offering, procedure['name'] , dateFrom, dateTo)

    # Print the observations
    printObservationValues(procedure['name'], observation_values)

    # Save the observations in a csv file
    saveToCSV(procedure['name'], observation_values)