#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MerakiPII Sample Script.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Zach Brewer"
__email__ = "zbrewer@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# example script that uses MerakiPII.PIICalls module to loop through PII identifiers and return PII Keys
# data from this API call/example can be used to make PII delete or restrict processing requests (these start with example19)
# Make sure to check the API Documentation - some attributes are for Systems Manager (SM) Orgs/Networks only

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#list-the-keys-required-to-access-personally-identifiable-information-pii-for-a-given-identifier_value

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getNetworkPIIKeys function in PII module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# from here on out, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['MY-DEFAULT']['API_KEY']
orgid = config['MY-DEFAULT']['ORG_ID']

# assign all ID and ID values from config.ini MULTIPLE-ID-VALUES section to a list
MY_LIST_VALUES = list(config.items('MULTIPLE-ID-VALUES'))

# set an indice value of 2 to assign every pair of IDENTIFIER and IDENTIFIER_TYPE from config.ini 
# MULTIPLE-ID-VALUES to a nested list
n_indices=2
# loop through all values in list loaded from MULTIPLE-ID-VALUES section of config.ini
for i in range(0, len(MY_LIST_VALUES), n_indices):
    # assign every nested pair to config_list1 and config_list2 respectively.
    # Note that this assigning 2 values like this is usually frowned upon, use w/ caution if reusing this code [zb]
    config_list1,config_list2 = MY_LIST_VALUES[i:i+n_indices]
    # set identifier_type to the value of config_list1
    identifier_type = (config_list1[1])
    # set identifier_value to the value of config_list2
    identifier_value = (config_list2[1])
    # simple print statement to let us know what IDs we are dealing with
    print( '\n\n' + 'Printing next API call for identifier_value type ' + '"' + identifier_type + '"' + ' and identifier_value ' + '"' + identifier_value + '"')

    # make an API call for each pair in config.ini MULTIPLE-ID-VALUES section passing in the pair of ID_type and ID
    MyMultipleOrgKeys = PIICalls.getOrgPIIKeys(apikey, orgid, identifier_type, identifier_value)
    # print output per API call in for loop using json.dumps
    print(json.dumps(MyMultipleOrgKeys, indent=4, sort_keys=False))
