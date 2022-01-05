# capstone
This is a collection of python and bash scripts that I wrote for my capstone project:

**OpenSky.py**  
This script is the heart of my capstone. It pulls aircraft telemetry data from the Open Sky network and indexes that data to Elasticsearch.

**ADSBSensor.py**  
Class that represents an ADS-B sensor object. Multiple object instantiations are made and their status information is indexed into Elasticsearch.

**ADSBCommand.py**  
This is the brains of the ADS-B operation. It reads a file containing state information about each FAA-operated ADS-B sensor, creates ADSBSensor objects for each record in the file, and then does some manipulation of those objects before writing them out to a file to be consumed by bulk_load_adsb.py

The `data/` directory contains a wealth of data that might be useful to others. Most notably, the `data/accidents/raw_json/` directory contains *30 years* of NTSB aviation accident reports. The raw json is pretty obnoxious to work with, so I wrote `bin/convert_accident_cases_to_ndjson.py` to parse those raw json files out, flatten the fields into dot-notation, and write them back out to `data/output/` as ndjson files ready for bulk importing (using the python Elasticsearch.helpers libraries...for some reason, the GUI drag-and-drop file import in Kibana chokes on these files).

The `mappings/` directory contains the mappings for the Open Sky index templates and data streams, and the NTSB accident index(es)
