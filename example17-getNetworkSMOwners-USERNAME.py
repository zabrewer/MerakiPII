# simple example script that uses MerakiPII.PIICalls module to get the Systems Manager Device ID for given PII attribute
# data from this API call/example can be used to make PII delete or restrict processing requests (these start with example19)
# Make sure to check the API Documentation - this call applies to Systems Manager (SM) Orgs/Networks only

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-owner-ids-associated-with-that-identifier

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getOrgSMDevicesForKey function in PIICalls module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# for this file and other examples, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['MDM-DEFAULT']['API_KEY']
networkid = config['MDM-DEFAULT']['NETWORK_ID']
identifier_value = config['MDM-DEFAULT']['IDENTIFIER_VALUE_USERNAME']
identifier_type = config['MDM-DEFAULT']['IDENTIFIER_TYPE_USERNAME']

print('\n')
print('**The Org/Network used in this call MUST be a Systems Manager enabled Org/Network**')
print('\n')
print('Making PII API Call to retrieve Systems Manager Owner ID for identifier_value type ' + '"' + identifier_type + '"' + ' with the value of '+ '"' + identifier_value + '"' + ': \n')
print('\n')

MyNetworkSMOwners = PIICalls.getNetworkSMOwnersForKey(apikey, networkid, identifier_type, identifier_value)
print(json.dumps(MyNetworkSMOwners, indent=4, sort_keys=False))