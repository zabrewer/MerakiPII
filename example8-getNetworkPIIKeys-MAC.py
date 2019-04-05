# simple example script that uses MerakiPII.PIICalls module to get all required to access PII for a given identifier_value
# data from this API call/example can be used to make PII delete or restrict processing requests (these start with example19)
# Make sure to check the API Documentation - some attributes are for Systems Manager (SM) Orgs/Networks only

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#list-the-keys-required-to-access-personally-identifiable-information-pii-for-a-given-identifier_value

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getNetworkPIIKeys function in PIICalls module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# from here on out, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['DEFAULT-KEYS-MAC']['API_KEY']
networkid = config['DEFAULT-KEYS-MAC']['NETWORK_ID']
identifier_type = config['DEFAULT-KEYS-MAC']['IDENTIFIER_TYPE']
identifier_value = config['DEFAULT-KEYS-MAC']['IDENTIFIER_VALUE']

print('\nAssociated PII Keys from this call can be used in PII delete or restrict processing requests.'
        '\n'
        'See "example19-SubmitNewOrgDelRequest-MAC" and above for PII delete or restrict processing requests.'
        '\n\n'
        'Making PII Key API call for identifier_value type ' + '"' + identifier_type + '"' + ' with the value of '+ '"' + identifier_value + '"' + ':'
        '\n...'
        )

MyNetworkPIIKeys = PIICalls.getNetworkPIIKeys(apikey, networkid, identifier_type, identifier_value)
print(json.dumps(MyNetworkPIIKeys, indent=4, sort_keys=False))