import argparse
import ADSBSensor
import csv
import random
from random import randint
from time import sleep

def setup_sensors(filename):
    adsb_sensors = {}
    # Read the CSV file that contains ADS-B sensor data
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # For each ADS-B row in CSV file, create ADSBSensor object
        for row in reader:
            obj = ADSBSensor.ADSBSensor(row['id'], row['lat'], row['lon'], row['city'], row['state'], row['tier'], row['offline'], row['healthy'], row['flux_cap'])
            adsb_sensors[obj.id] = obj
    return adsb_sensors
    
def write_sensor_status(filename, status):
    pass

def poll_sensors(sensor_list):
    # Randomize access to the objects in this dictionary
    keys = list(sensor_list.keys())
    random.shuffle(keys)
    for key in keys:
        print(sensor_list[key].status())

def parse_args():
    parser = argparse.ArgumentParser(prog='ADSBCommand.py', description='Parse command-line arguments')
    parser.add_argument('--add-latency', dest='latency', action='store', help='Add latency to the return of ADSBSensor object\'s status')
    parser.add_argument('--sensor-offline', dest='offline', action='store_false', help='Make the sensor start in Offline mode (True or False)')
    parser.add_argument('--flux-capacitor', dest='flux_cap', action='store', type=float, help='Set the initial flux capacitor value')
    parser.parse_args()

def main():
    parse_args()
    # Retrieve list of ADS-B sensors as a dictionary
    adsb_sensors = setup_sensors('data/adsb.csv')
    poll_sensors(adsb_sensors)

if __name__ == '__main__':
    main()
    