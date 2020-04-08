"""
TODO:
- Analyse the internet speed based on time (Location).
- Analysis based on average speed per telco (Location)
- Sort best telcos on average speed collected (Location)
- List poorest networks to avoid (Location)
- Compare 3G over 4G average speed (Location)
- Compare 3G networks providers (Location)
- Compare 4G networks providers (Location)
- Recommend the best network for working at home (Location).
- Recommend the best 4G network for mobile network (Location).
- Recommend the best 3G network to use according to location (Location)

- CSV to JSON
- Remove unecessary data
"""
import pandas as pd
from os import path
import json

this_directory = path.abspath(path.dirname(__file__))
CSV_PATH = '{}/resources/data/data.csv'.format(this_directory)

# Network types
HSPA = ['airtel', 'mtn']
LTE = ['airtel', 'mtn', 'kt', 'mango', 'fastnet', 'tnsp', 'bk',
       'netlink', 'rtn', 'trueconnect', 'CbNet']
WIRELESS = ['axiom']
FIBER = ['liquid', 'canal']


def csv_to_json():
    df = pd.read_csv(CSV_PATH)
    return df.to_json(orient='records')


JSON_ITEMS = json.loads(csv_to_json())


def get_location():
    location = [item['location_cleaned'] for item in JSON_ITEMS]
    return list(dict.fromkeys(location))


def get_telcos():
    isp = [item['isp_cleaned'] for item in JSON_ITEMS]
    return list(dict.fromkeys(isp))


# TODO filter by Telcos
def filter_by_telcos():
    # 3G network
    hspa = dict()
    for isp in HSPA:
        hspa[isp] = [item
                     for item in JSON_ITEMS
                     if isp in item['text'].lower() and
                     '4g' not in item['text'].lower()]

    # 4G network
    lte = dict()
    for isp in LTE:
        if isp in ['airtel', 'mtn']:
            lte[isp] = [item
                        for item in JSON_ITEMS
                        if isp in item['text'].lower() and
                        '4g' in item['text'].lower()]
        lte[isp] = [item
                    for item in JSON_ITEMS
                    if isp in item['text'].lower()]

    # wireless network
    wireless = dict()
    for isp in WIRELESS:
        wireless[isp] = [item
                         for item in JSON_ITEMS
                         if isp in item['text'].lower()]

    # fiber network
    fiber = dict()
    for isp in FIBER:
        fiber[isp] = [item
                      for item in JSON_ITEMS
                      if isp in item['text'].lower()]

    return {
            'hspa': hspa,
            'lte': lte,
            'wireless': wireless,
            'fiber': fiber
    }


def filter_location():
    pass
