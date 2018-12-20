import sqlite3
import json
import os


def crime_info(ini_Latitude, ini_Longitude, delta_Latitude=0.003074928502714, delta_Longitude=0.002123443787347):
    db_file = os.getcwd() + "/crime_data/crime.db"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    crime_types = ['BURGLARY-RESIDENCE', 'BURGLARY-NONRES',\
    'AUTO THEFT', 'ROBBERY-PEDESTRIAN',\
    'MANSLAUGHTER', 'ROBBERY-COMMERCIAL',\
    'HOMICIDE', 'LARCENY-NON VEHICLE',\
    'AGG ASSAULT', 'LARCENY-FROM VEHICLE',\
    'ROBBERY-RESIDENCE']
    crime_stat = {}
    for crime_type in crime_types:

        cursor.execute('''SELECT *FROM crime_data \
        WHERE ((abs(Latitude-?)<?) \
        and (abs(Longitude-?)<?)\
        and ([UCR Literal]=?));''', \
        (ini_Latitude, delta_Latitude, \
        ini_Longitude, delta_Longitude, \
        crime_type))

        data = cursor.fetchall()
        crime_stat[crime_type] = len(data)

    db.close()
    total_crime = 0
    for value in crime_stat.values():
        total_crime += value
    crime_stat['total_crime'] = total_crime 
    crime_json = json.dumps(crime_stat)
    return crime_json

if __name__ == "__main__":

    crime_json = crime_info(ini_Latitude=10, ini_Longitude=10, delta_Latitude=100, delta_Longitude=100)
    print(crime_json)
