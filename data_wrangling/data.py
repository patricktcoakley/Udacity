"""
UDACITY
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function 
with the element as an argument. You should return a dictionary, containing the 
shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular 
key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array 
      are floats and not strings.
- if the second level tag "k" value contains problematic characters, it should 
  be ignored
- if the second level tag "k" value starts with "addr:", it should be added to 
  a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains 
  ":", you can process it in a way that you feel is best. For example, you 
  might split it into a two-level dictionary like with "addr:", or otherwise 
  convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

OSM_FILE = "sanfrancisco.osm"

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

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
    if street not in expected and street is not None:
        if street.group() in mapping.keys():
            name = re.sub(street.group(), mapping[street.group()], name)
    return name

def shape_element(element):
    node = {}
    address = {}
    if element.tag == 'node' or element.tag == 'way':
        for key in element.attrib.keys():
            value = element.attrib[key]
            node['type'] = element.tag
            if key in CREATED:
                if not 'created' in node.keys():
                    node['created'] = {}
                node['created'][key] = value
            elif key == 'lat' or key == 'lon':
                if not 'pos' in node.keys():
                    node['pos'] = [0.0, 0.0]
                old_position = node['pos']
                if key == 'lat':
                    new_position = [float(value), old_position[1]]
                else:
                    new_position = [old_position[0], float(value)]
                node['pos'] = new_position
            else:
                node[key] = value
            for tag in element.iter('tag'):
                tag_key = tag.attrib['k']
                tag_value = tag.attrib['v']
                if problemchars.match(tag_key):
                    continue
                elif tag_key.startswith('addr:'):
                    address_key = tag.attrib['k'][len('addr:'):]
                    if lower_colon.match(address_key):
                        continue
                    # Updates all 'state' values to 'CA'
                    elif address_key == 'state':
                        node[address_key] = "CA"
                    # Updates all 'street' values using function
                    # created in 'audit.py
                    elif address_key == 'street':
                        node[address_key] = update_name(tag_value, mapping)
                    # Updates all 'postcode' values
                    elif address_key == 'postcode':
                        zipcode = tag_value
                        # Regex that filters 5-digit groups
                        new_zipcode = re.findall(r'(\d{5})$', zipcode)
                        if len(new_zipcode) > 0:
                            node[address_key] = new_zipcode[0]
                    else:
                        address[address_key] = tag_value
                elif lower_colon.match(tag_key):
                    node[tag_key] = tag_value
                else:
                    node[tag_key] = tag_value
        for tag in element.iter('nd'):
            if not 'node_refs' in node.keys():
                node['node_refs'] = []
            node_refs = node['node_refs']
            node_refs.append(tag.attrib['ref'])
            node['node_refs'] = node_refs

        if address:
            node['address'] = address
        return node
    else:
        return None

def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

process_map(OSM_FILE, pretty=True)