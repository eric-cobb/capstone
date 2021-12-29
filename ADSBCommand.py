import argparse
import ADSBSensor
import csv
import random
from random import randint
from time import sleep

add_latency = False

def setup_sensors(filename):
    adsb_sensors = {}
    # Read the CSV file that contains ADS-B sensor data
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # For each ADS-B row in CSV file, create ADSBSensor object
        for row in reader:
            if row['offline'] == '':
                row['offline'] = False
            if row['healthy'] == '':
                row['healthy'] = True
            if add_latency:
                latency = random.uniform(0, 0.5)
            else:
                latency = 0
            adsb_obj = ADSBSensor.ADSBSensor(row['id'], row['lat'], row['lon'], row['city'], row['state'], row['tier'], row['offline'], row['healthy'], latency, row['flux_cap'])
            adsb_sensors[adsb_obj.id] = adsb_obj
    return adsb_sensors
    
def write_sensor_status(filename, status):
    #filename.write('{"index": {"_index": "adsb-sensors"}}\n')
    filename.write(status + '\n')

def randomize_list_keys(adsb_list):
    keys = list(adsb_list.keys())
    random.shuffle(keys)
    return keys

def poll_sensors(sensor_list, file=None):
    # Randomize access to the objects in this dictionary
    keys = randomize_list_keys(sensor_list)
    if file:
        fd = open(file, "w")
        for key in keys:
            write_sensor_status(fd, sensor_list[key].get_status())
        fd.close()
    else:
        for key in keys:
            print(sensor_list[key].get_status())

def parse_args():
    parser = argparse.ArgumentParser(prog='ADSBCommand.py', description='Parse command-line arguments')
    parser.add_argument('--add-latency', dest='latency', action='store_true', help='Add latency when initializing ADSBSensor objects')
    parser.add_argument('--sensor-offline', dest='offline', action='store_false', help='Make the sensor start in Offline mode (True or False)')
    parser.add_argument('--sensor', dest='sid', action='store', help='The sensor ID to change')
    parser.add_argument('--flux-capacitor', dest='flux_cap', action='store', type=float, help='Set the initial flux capacitor value')
    parser.add_argument('--error-rate', dest='error_rate', action='store', help='Percentage of sensors to assign some kind of error')
    parser.add_argument('--file', dest='file', action='store', help='Write the output to this file')
    return parser.parse_args()

def assign_errors(adsb_sensors, rate):
    num_to_change = round(len(adsb_sensors) * (int(rate)/100))
    to_be_changed = random.choices(list(adsb_sensors.items()), k=num_to_change)
    for obj in to_be_changed:
        obj[1].set_random_error()

def main():
    global add_latency
    args = parse_args()

    if args.latency:
        add_latency = args.latency

    # Retrieve list of ADS-B sensors as a dictionary
    adsb_sensors = setup_sensors('data/adsb/adsb.csv')

    if args.sid:
        if args.offline:
            adsb_sensors[args.sid].set_offline(True)
        if args.flux_cap:
            adsb_sensors[args.sid].set_flux_cap(args.flux_cap)
    if args.error_rate:
            assign_errors(adsb_sensors, args.error_rate)  
    if args.file:
        poll_sensors(adsb_sensors, args.file)
    else:
        poll_sensors(adsb_sensors)

if __name__ == '__main__':
    main()
    