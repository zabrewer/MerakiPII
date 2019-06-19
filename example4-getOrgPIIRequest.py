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

# simple example script that uses MerakiPII to get a SINGLE PII Request for a given Org
# Must have the requestID from getOrgPIIRequests (don't confuse these two functions)
# don't confuse getNetworkPIIRequest with getNetworkPIIRequests
# or getOrgPIIRequest with getOrgPIIRequests

# API Documentation for this call:  https://dashboard.meraki.com/api_docs#return-a-pii-request

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getOrgPIIRequest function in PIICalls module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# for this file and other examples, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['MY-DEFAULT']['API_KEY']
orgid = config['MY-DEFAULT']['ORG_ID']
requestid = config['MY-DEFAULT']['PII_ID']

MyOrgPIIRequest = PIICalls.getOrgPIIRequest(apikey, orgid, requestid)
print('The following uses the Python json module to format and print the results of a single existing PII Request for the given org: \n')
print(json.dumps(MyOrgPIIRequest, indent=4, sort_keys=False))
