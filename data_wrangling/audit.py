"""
UDACITY
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes 
	needed to fix the unexpected street types to the appropriate ones in the 
	expected list. You have to add mappings only for the actual problems you 
	find in this OSMFILE, not a generalized solution, since that may and will 
	depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should 
    return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json

OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
state_type_re = re.compile(r'.*', re.IGNORECASE)


expected = [ "Street", "Avenue", "Boulevard", "Drive", "Court", "Place", 
			"Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Highway", 
			"Terrace", "Way", "Alley", "Mission", "Mason", "Embarcadero", 
			"Broadway", "Circle", "Plaza", "39", "B", "D", "West", "Francisco", 
			"Ferlinghetti" ]

mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Drv": "Drive",
            "Drv.": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "Pl" : "Place",
            "Pl." : "Place",
            "Sqr": "Square",
            "Sqr.": "Square",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Rd": "Road",
            "Rd.": "Road",
            "Pkwy": "Parkway",
            "Pkwy.": "Parkway",
            "Hwy": "Highway",
            "Hwy.": "Highway"

}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    street = street_type_re.search(name)
    if street not in expected:
        if street.group() in mapping.keys():
            name = re.sub(street.group(), mapping[street.group()], name)
    return name

audited_map = audit(OSMFILE)

for audited_map, ways in audited_map.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name