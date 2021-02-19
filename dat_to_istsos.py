import subprocess
import os

host = "http://127.0.0.1/istsos"
service = "meteogr"
full_path = os.path.abspath("stations_dat/")

for station_file in os.listdir(folder_source):
    station_name = station_file.split("_2")[0]

    # Use existing script that is already provided
    # http://istsos.org/en/trunk/doc/insert.html
    subprocess.run([
        "python3", "scripts/csv2istsos.py",
        "-p", station_name, "-u", host, "-s", service, "-w", full_path
        ], cwd = "/usr/local/istsos")
