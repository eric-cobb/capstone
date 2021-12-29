from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import streaming_bulk
import os.path
import configparser
import sys

def create_index(client):
    client.indices.create(
        index="adsb-sensors",
        settings={
            "number_of_shards": 1
        },
        ignore=400
    )

def gen_actions(file):
    fd = open(file)
    for line in fd:
        yield {
            "_index": "adsb-sensors",
            "_source": line
        }

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]

def main(arg):
    # These two lines were strictly for convenience when bouncing between different
    # credentials and API keys. You can omit this and simply configure the ES client
    # below with normal username/password credentials
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/../cfg/es.ini')
    
    # This can be configured with simple username/password credentials instead of
    # the config file items
    es = Elasticsearch(
        cloud_id=config['ECOBB-CCS']['cloud_id'],
        api_key=(config['ECOBB-CCS']['apikey_id'], config['ECOBB-CCS']['apikey'])
    )

    # Create the index and change the mapping fields limit
    create_index(es)

    success, failed = 0, 0
    errors = []
    file = arg
    for ok, item in streaming_bulk(es, gen_actions(file)):
        if not ok:
            errors.append(item)
            failed += 1
        else:
            success += 1
    print(success, failed)




if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        main(filename)
    except IndexError:
        print("No filename given")