"""
Main code to generate ADS-B sensor objects from an initial file list, 
interact with those objects, and write their status to either a file
or stdout

Attributes
----------
add_latency : bool
    Whether or not to add latency to the response from a sensor 
    object's .get_status() method
"""

import argparse
import ADSBSensor
import csv
import random
from random import randint
from time import sleep
import os.path

add_latency = False

def assign_errors(adsb_sensors, rate):
    """
    Adds an error state to a random subset (percentage equal to 'rate')
    of sensors 
    
    Parameters
    ----------
    adsb_sensors : dict
        The list of sensors to iterate through
    rate : int
        The percentage of sensors to which to apply errors
    """

    for obj in random_sample(adsb_sensors, rate):
        obj[1].set_random_error()

def assign_flux_values(adsb_sensors, rate):
    """
    Iterate through the dictionary of sensors at random and at a 
    percentage equal to 'rate' and change their flux capacitor 
    values
    
    Parameters
    ----------
    adsb_sensors : dict
        The list of sensors to iterate through
    rate : int
        The percentage of sensors to which to apply flux capacitor
        values
    """

    for obj in random_sample(adsb_sensors, rate):
        # Set flux_capacitor value randomly between 0.92 and 1.99
        obj[1].set_flux_cap(round(random.uniform(0.92, 1.99), 2))

def parse_args():
    """
    Parse the command-line arguments
    """

    parser = argparse.ArgumentParser(prog='ADSBCommand.py', description='Parse command-line arguments')
    # Add latency to every sensor object's .get_status() response
    parser.add_argument('--add-latency', dest='latency', action='store_true', help='Add latency when initializing ADSBSensor objects')
    # Set the sensor to be 'offline'. Must be paired with --sensor, 
    # otherwise will be silently ignored
    parser.add_argument('--sensor-offline', dest='offline', action='store_true', help='Make the sensor start in Offline mode (True or False)')
    # The id of the sensor to manipulate
    parser.add_argument('--sensor', dest='sid', action='store', help='The sensor ID to change')
    # The flux_capacitor value to be set in the object. Must be paired
    # with --sensor, otherwise will be silently ignored
    parser.add_argument('--flux-capacitor', dest='flux_cap', action='store', type=float, help='Set the initial flux capacitor value')
    # Assign a flux_capacitor value to a random sampling of sensors
    parser.add_argument('--random-flux', dest='flux_rate', action='store', help='Assign random flux capacitor values to a random sample of sensors')
    # Assign a random error to a random sampling of sensors
    parser.add_argument('--error-rate', dest='error_rate', action='store', help='Percentage of sensors to assign some kind of error')
    # The file to which to write sensor status information
    parser.add_argument('--file', dest='file', action='store', help='Write the output to this file')
    return parser.parse_args()

def poll_sensors(sensor_list, file=None):
    """
    Iterate through the dictionary of sensors. If 'file' is given, 
    write the output to file; if not, write to stdout
    
    Parameters
    ----------
    sensor_list : dict
        The list of sensors to iterate through
    file : str
        The filename to which to write the output, if given
    """

    keys = randomize_dict_keys(sensor_list)
    if file:
        fd = open(file, "w")
        for key in keys:
            write_sensor_status(fd, sensor_list[key].get_status())
        fd.close()
    else:
        for key in keys:
            print(sensor_list[key].get_status())

def random_sample(adsb_sensors, rate):
    """
    Generate a random subset of ADS-B sensors and return
    
    Parameters
    ----------
    adsb_sensors : dict
        The list of sensors to iterate through
    rate : int
        The percentage of sensors to which to apply errors
    """

    # Express 'rate' as a percentage and multiply by the number of 
    # sensors in the dictionary to get the number of sensors to be 
    # changed
    num_to_change = round(len(adsb_sensors) * (int(rate)/100))
    # Sampling of the actual sensor objects to be changed, based 
    # on 'rate'
    random_sample = random.choices(list(adsb_sensors.items()), k=num_to_change)
    return random_sample

def randomize_dict_keys(adsb_dict):
    """
    Randomize the dictionary keys to be used when randomizing access 
    to the sensors (e.g. when assigning random errors)

    Parameters
    ----------
    adsb_dict : dict
        The dictionary object containing the sensor objects
    """

    keys = list(adsb_dict.keys())
    random.shuffle(keys)
    return keys

def setup_sensors(filename):
    """
    Read sensor object information from the given file and return
    a dictionary of ADSBSensor objects

    Parameters
    ----------
    filename : str
        The file from which to read ADS-B sensor data
    """

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

# Not currently used, though was intended to be used to persist 
# sensor states between executions    
def write_sensor_status(filename, status):
    """
    Write sensor object status information to a file

    Parameters
    ----------
    filename : str
        The file to which to write ADS-B sensor data
    status : str
        The status information line expressed as NDJSON (for bulk
        loading into ES)
    """
    filename.write(status + '\n')

def main():
    global add_latency
    args = parse_args()

    if args.latency:
        add_latency = args.latency

    # Retrieve list of ADS-B sensors as a dictionary
    adsb_sensors = setup_sensors(os.path.dirname(os.path.abspath(__file__)) + '/data/adsb/adsb.csv')

    if args.error_rate:
        assign_errors(adsb_sensors, args.error_rate)
    if args.flux_rate:
        assign_flux_values(adsb_sensors, args.flux_rate)
    if args.sid:
        if args.offline:
            adsb_sensors[args.sid].set_offline(True)
        if args.flux_cap:
            adsb_sensors[args.sid].set_flux_cap(args.flux_cap) 
    if args.file:
        poll_sensors(adsb_sensors, args.file)
    else:
        poll_sensors(adsb_sensors)

if __name__ == '__main__':
    main()
    