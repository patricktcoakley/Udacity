''' This was just a simple script I played around with
to get an idea of what the data was going to look like
as I started the project, and it really is just a way
to output data based on regex similar to some of the
exercises in the course'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("sample.osm", "r")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

zip_type_re = re.compile(r'([9][4][1][0-9][0-9])', re.IGNORECASE)
zip_types = defaultdict(int)

state_type_re = re.compile(r'.*', re.IGNORECASE)
state_types = defaultdict(int)

city_type_re = re.compile(r'.*', re.IGNORECASE)
city_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def audit_zip_type(zip_types, zip_code):
    m = zip_type_re.search(zip_code)
    if m:
        zip_type = m.group()

        zip_types[zip_type] += 1

def audit_state_type(state_types, state):
    m = state_type_re.search(state)
    if m:
        state_type = m.group()

        state_types[state_type] += 1

def audit_city_type(city_types, city):
    m = city_type_re.search(city)
    if m:
        city_type = m.group()

        city_types[city_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def is_zip_code(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

def is_state(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state")

def is_city(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:city")


def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])

        elif is_zip_code(elem):
            audit_zip_type(zip_types, elem.attrib['v'])

        elif is_state(elem):
            audit_state_type(state_types, elem.attrib['v'])

        elif is_city(elem):
            audit_city_type(city_types, elem.attrib['v'])

    # print('Stree types: ')
    # print_sorted_dict(street_types)
    print('\nZip codes: ')
    print_sorted_dict(zip_types)
    # print('\nCities: ')
    # print_sorted_dict(city_types)
    # print('\nState: ')
    # print_sorted_dict(state_types)

if __name__ == '__main__':
    audit()