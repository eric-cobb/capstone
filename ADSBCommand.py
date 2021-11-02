import ADSBSensor
import csv
import random
from random import randint
from time import sleep

adsb_sensors = []

def setup():
    global adsb_sensors

    # Read the CSV file that contains ADS-B sensor data
    with open('data/adsb.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # For each ADS-B row in CSV file, create ADSBSensor object
        for row in reader:
            adsb_sensors.append(ADSBSensor.ADSBSensor(row['id'], row['lat'], row['lon'], row['city'], row['state'], row['tier']))

def poll_sensors():
    global adsb_sensors

    adsb_copy = adsb_sensors.copy()
    random.shuffle(adsb_copy)
    while len(adsb_copy) != 0:
        print(adsb_copy.pop().status())

if __name__ == '__main__':
    setup()
    poll_sensors()
    