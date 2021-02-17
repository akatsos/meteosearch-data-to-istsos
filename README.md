# meteosearch-data-to-istsos

A number of scripts to:
* Parse daily data from http://meteosearch.meteo.gr
* Convert the downloaded data to text/csv;subtype=istSOS
* Insert the data to an IstSOS instance (http://istsos.org/en/latest/doc/index.html)

Usage:
1. Get all the stations and their information from the meteosearch website. (get_all_stations.py)
2. Read the stations from the .csv created from the previous step and download all daily data for each one. (station_parser.py)
3. Convert the created .csv files to the .dat format that IstSOS supports. (csv_to_dat.py)
4. Add meteo service to IstSOS (istsos_add_meteo_service.py)
5. Add procedures to IstSOS (istsos_add_procedures.py)
6. Add measurements for each procedure to IstSOS (dat_to_istsos.py)

Notes:
* Default: Selected year is 2020 for all stations in Greece
* Various changes could be made to the scripts (eg. get data for more years)
