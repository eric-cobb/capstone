"""
Pulls data from the Open Sky network and inserts it into ES using the
Elasticsearch.helpers bulk() method
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk, streaming_bulk
from opensky_api import OpenSkyApi
import json
import configparser
from datetime import datetime
import os

def sanitize_str(field):
    """
    Strip all whitespace from the string. Some of the data has extra
    space around some of the values which messes with the tokenizer
    """

    if field is None:
        field = ""
    return field.strip()

def sanitize_num(field):
    """
    Numeric fields need to contain a number, so if they contain the 
    empty string, make it a 0
    """

    if field is None:
        field = 0
    return field

def convert_source(field):
    """
    Map numeric values for the position/telemetry source to string
    representations of the source that actually makes sense to 
    non-computers (aka humans)
    """

    if (field == 0): 
        field = 'ADS-B'
    elif (field == 1):
        field = 'ASTERIX'
    elif (field == 2):
        field = 'MLAT'
    elif (field == 3):
        field = 'FLARM'
    return field

# DO NOT USE THIS METHOD
def create_index(client):
    """
    -- DEPRECATED --
    Creates the index and its mapping (if necessary). This method is 
    no longer used. Create the "open-sky" index/data stream with the 
    .mapping files found in the "mappings/" directory
    """
    client.indices.create(
        index="sky-traffic-000001",
        settings={"number_of_shards": 1},
        mappings={
            "properties": {
                "@timestamp": {"type": "date"},
                "icao_code": {"type": "keyword"},
                "callsign": {"type": "keyword"},
                "origin_country": {"type": "keyword"},
                "baro_altitude": {"type": "long"},
                "geo_altitude": {"type": "long"},
                "heading": {"type": "short"},
                "speed": {"type": "short"},
                "vertical_speed": {"type": "short"},
                "location": {"type": "geo_point"},
                "squawk": {"type": "keyword"},
                "last_position_report": {"type": "date"},
                "last_contact": {"type": "date"},
                "on_ground": {"type": "boolean"},
                "spi": {"type": "keyword"},
                "position_source": {"type": "keyword"}
            }
        },
        ignore=400
    )

def gen_actions(opensky_states):
    """
    Generator method that takes the open-sky state dictionary object  
    and yields the bulk data output expected by the Elasticsearch.helpers 
    bulk() method

    Parameters
    ----------
    opensky_states : dict
        Contains all the state vector (telemetry) data for multiple aircraft
    """

    for sky_state in opensky_states.states:
        doc = {
	    "_index": "open-sky", # Changed from 'sky-traffic-000001' to use Data Stream instead of Index - ecobb 12/27/2021
            "pipeline": "latlon-to-csa",
            "_op_type": "create", # _op_type of 'create' (versus, say, 'index') is required for data streams
            "_source": {
                "@timestamp": datetime.fromtimestamp(sanitize_num(sky_state.last_contact)),
                "icao_code": sky_state.icao24,
	            "callsign": sanitize_str(sky_state.callsign), # can be null
                "origin_country": sky_state.origin_country,
	            "baro_altitude": round(sanitize_num(sky_state.baro_altitude) * 3.28084), # can be None, ft
		        "geo_altitude": round(sanitize_num(sky_state.geo_altitude) * 3.28084), # can be None, ft
	            "heading": round(sanitize_num(sky_state.heading)), # can be None
		        "speed": round(sanitize_num(sky_state.velocity) * 1.94384), # can be None, mph
		        "vertical_speed": round(sanitize_num(sky_state.vertical_rate) * 196.85), # can be None, fpm
	            "squawk": sanitize_num(sky_state.squawk), # can be None
		        "last_position_report": datetime.fromtimestamp(sanitize_num(sky_state.time_position)), # can be None 
	            "last_contact": datetime.fromtimestamp(sanitize_num(sky_state.last_contact)), # can be None
	            "on_ground": sky_state.on_ground,
	            "spi": sky_state.spi,
	            "position_source": convert_source(sky_state.position_source)
            }
        }
        lat = sanitize_num(sky_state.latitude)
        lon = sanitize_num(sky_state.longitude)
        if lat not in ("", "0") and lon not in ("", "0"):
            doc["_source"]["location"] = {"lat": float(lat), "lon": float(lon)}
        yield doc

def main():
    config = configparser.ConfigParser()
    # Changed this to use the os.path method without testing it, so
    # if the ES authentication fails this is a good place to start
    config.read(os.path.dirname(os.path.abspath(__file__)) + 'cfg/es.ini')

    api = OpenSkyApi()
    
    es = Elasticsearch(
        cloud_id=config['DEFAULT']['cloud_id'],
        api_key=(config['NEW']['apikey_id'], config['NEW']['apikey'])
    )

    # Get only the air traffic within bounding box of CONUS
    opensky_states = api.get_states(bbox=(24.7433195, 49.3457868, -124.7844079, -66.9513812))
    status = bulk(es, gen_actions(opensky_states))
    print(status)

if __name__ == '__main__':
    main()