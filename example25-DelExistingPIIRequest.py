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

# simple example script that uses MerakiPII.PIICalls module to get all PII Requests for a given Organization
# A 404/null means the API call was successful but no PII call has been made for the network/org  
# PII delete and/or restrict processing examples start with example19-SubmitNewOrgDelRequest-MAC.py
# run those examples against a given network/org if you need data to return for this and other examples
# if the request worked, you should receive 'PII Deleted Successfully' as a response

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#delete-a-restrict-processing-pii-request

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see submitOrgPIIRequest function in PIICalls module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# for this file and other examples, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
# it would be helpful to read through the API documentation for this call/function
# username usually applies only to a WIFI network with a splash page and local (Meraki) auth
# basically sending a DELETE PII request to a WIFI network/org will remove
#  user's username and other data under WIRELESS --> SPLASH LOGINS  in the Meraki Dashboard
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['DEFAULT-KEYS-EMAIL']['API_KEY']
orgid = config['DEFAULT-KEYS-EMAIL']['ORG_ID']
# please note this ONLY applies to requestIDs of type 'Restrict Procressing'
requestid = config['MY-DEFAULT']['PII_ID']

MyDelPIIRequest = PIICalls.delOrgPIIRequest(apikey, orgid, requestid)
print(json.dumps(MyDelPIIRequest, indent=4, sort_keys=False))
