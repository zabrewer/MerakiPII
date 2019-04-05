# simple example script that uses MerakiPII.PIICalls module to get all PII Requests for a given Organization
# A 404/null means the API call was successful but no PII call has been made for the network/org  
# PII delete and/or restrict processing examples start with example19-SubmitNewOrgDelRequest-MAC.py
# run those examples against a given network/org if you need data to return for this and other examples

# API Documentation for this call:  https://dashboard.meraki.com/api_docs#list-the-pii-requests-for-this-network-or-organization

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getOrgPIIRequests function in PIICalls module for details and arguments

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

MyOrgPIIRequests = PIICalls.getOrgPIIRequests(apikey, orgid)
print('The following uses the Python json module to format and print the results of MyOrgPIIRequests: \n')
print('If no PII delete or restrict processing requests have been made for the given OrgID, you will not get data \n')

print(json.dumps(MyOrgPIIRequests, indent=4, sort_keys=False))
