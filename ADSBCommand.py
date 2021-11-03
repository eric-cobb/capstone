import argparse
import ADSBSensor
import csv
import random
from random import randint
from time import sleep

adsb_sensors = {}

def setup():
    global adsb_sensors

    # Read the CSV file that contains ADS-B sensor data
    with open('data/adsb.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # For each ADS-B row in CSV file, create ADSBSensor object
        for row in reader:
            obj = ADSBSensor.ADSBSensor(row['id'], row['lat'], row['lon'], row['city'], row['state'], row['tier'])
            adsb_sensors[obj.id] = obj

def poll_sensors():
    global adsb_sensors

    # Randomize access to the objects in this dictionary
    adsb_copy = adsb_sensors.copy()
    keys = list(adsb_copy.keys())
    random.shuffle(keys)
    
    for key in keys:
        print(adsb_copy[key].status())

def parse_args():
    parser = argparse.ArgumentParser(prog='ADSBCommand.py', description='Parse command-line arguments')
    parser.add_argument('--add-latency', dest='latency', action='store', help='Add latency to the return of ADSBSensor object\'s status')
    parser.add_argument('--sensor-offline', dest='offline', action='store_false', help='Make the sensor start in Offline mode (True or False)')
    parser.add_argument('--flux-capacitor', dest='flux_cap', action='store', type=float, help='Set the initial flux capacitor value')
    parser.parse_args()

def main():
    global adsb_sensors
    actions = ['set_health', 'set_flux_cap', 'set_offline']
    poll_sensors()

if __name__ == '__main__':
    parse_args()
    setup()
    main()
    