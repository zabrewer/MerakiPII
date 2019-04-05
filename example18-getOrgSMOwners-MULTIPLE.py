# example script that uses MerakiPII.PIICalls module to loop through PII identifiers for Systems Manager and return SM Owner ID
# process is very much the same for SM Device ID, just change the function called in the next-to-last line to getOrgSMDevicesID
# data from this API call/example can be used to make PII delete or restrict processing requests (these start with example19)
# Make sure to check the API Documentation - this call applies to Systems Manager (SM) Orgs/Networks only

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-owner-ids-associated-with-that-identifier

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getOrgSMOwners function in PII module for details and arguments

# see the 1st example (example1-getOrgPIIRequests.py) for various ways to assign values for API calls
# from here on out, we are using config.ini file for values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
import configparser
import json

# load config.ini and assign config variables from appropriate section to variables
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['MDM-DEFAULT']['API_KEY']
orgid = config['MDM-DEFAULT']['ORG_ID']

# assign all ID and ID values from config.ini MULTIPLE-ID-VALUES section to a list
MY_LIST_VALUES = list(config.items('MDM-VALUES'))

# set an indice value of 2 to assign every pair of IDENTIFIER and IDENTIFIER_TYPE from config.ini 
# MULTIPLE-ID-VALUES to a nested list
n_indices=2
# loop through all values in list loaded from MULTIPLE-ID-VALUES section of config.ini
for i in range(0, len(MY_LIST_VALUES), n_indices):
    # assign every nested pair to config_list1 and config_list2 respectively.  \
    # Note that this is usuall frowned upon, use w/ caution if reusing this code [zb]
    config_list1,config_list2 = MY_LIST_VALUES[i:i+n_indices]
    # set identifier_type to the value of config_list1
    identifier_type = (config_list1[1])
    # set identifier to the value of config_list2
    identifier = (config_list2[1])
    # simple print statement to let us know what IDs we are dealing with
    print( '\n\n' + 'Printing next API call for identifier type ' + '"' + identifier_type + '"' + ' and identifier ' + '"' + identifier + '"')

    # make an API call for each pair in config.ini MULTIPLE-ID-VALUES section passing in the pair of ID_type and ID
    MyMultipleOrgSMKeys = PIICalls.getOrgSMOwnersForKey(apikey, orgid, identifier_type, identifier)
    # print output per API call in for loop using json.dumps
    print(json.dumps(MyMultipleOrgSMKeys, indent=4, sort_keys=False))
