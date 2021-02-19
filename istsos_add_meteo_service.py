import requests
import json

url = "http://127.0.0.1/istsos/wa/istsos/services"

# Create service
service = {
    "service": "meteogr"
}

r = requests.post(url, data=json.dumps(service))
print("Service: ", r.text)

# Add degrees unit of measurement
degrees_uom = {
    "name":"\u00b0",
    "description":"degrees"
}

r = requests.post(url + f"/{service['service']}/uoms", data=json.dumps(degrees_uom))
print("Degrees UOM: ", r.text)

# Add km/h unit of measurement
kmh_uom = {
    "name":"km/h",
    "description":"kilometers per hour"
}

r = requests.post(url + f"/{service['service']}/uoms", data=json.dumps(kmh_uom))
print("KMH UOM: ", r.text)

# Add wind-direction observed property
wind_direction_op= {
    "name":"air-wind-direction",
    "definition":"urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:direction",
    "description":"wind direction",
    "constraint":{}
}

r = requests.post(url + f"/{service['service']}/observedproperties", data=json.dumps(wind_direction_op))
print("OP: ", r.text)