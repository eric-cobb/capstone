# capstone
This is a collection of python and bash scripts that I wrote for my capstone project:

**OpenSky.py**
This script is the heart of my capstone. It pulls aircraft telemetry data from the Open Sky network and indexes that data to Elasticsearch.

**ADSBSensor.py**
Class that represents an ADS-B sensor object. Multiple object instantiations are made and their status information is indexed into Elasticsearch.

**ADSBCommand.py**
This is the brains of the ADS-B operation. It reads a file containing state information about each FAA-operated ADS-B sensor, creates ADSBSensor objects for each record in the file, and then does some manipulation of those objects before writing them out to a file to be consumed by bulk_load_adsb.py
