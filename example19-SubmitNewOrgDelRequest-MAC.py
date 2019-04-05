# example script that uses MerakiPII.PIICalls module to submit a new DELETE or RESTRICT PROCESSING PII request given PII attribute
# Make sure to check the API Documentation - there are various valid attribute combinations when making this request

# API Documentation for this call:  
# https://dashboard.meraki.com/api_docs#submit-a-new-delete-or-restrict-processing-pii-request

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
# mac usually applies only to a WIFI network with a splash page and local (Meraki) auth
# basically sending a DELETE PII request to a WIFI network/org will remove
#  user's mac and other data under WIRELESS --> SPLASH LOGINS  in the Meraki Dashboard
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['DEFAULT-KEYS-MAC']['API_KEY']
orgid = config['DEFAULT-KEYS-MAC']['ORG_ID']
# set "action" (delete or restrict processing) argument directly rather than read from config.ini
# restrict processing - only applies to smDeviceID, smUserId, or mac
action = 'delete'
# set IDENTIFIER_TYPE to type 'mac'
identifier_type = config['DELETE-AND-RESTRICT-DATA']['IDENTIFIER_TYPE_MAC']
# set IDENTIFIER to an actual mac address value in config.ini
identifier_value = config['DELETE-AND-RESTRICT-DATA']['IDENTIFIER_VALUE_MAC']
# datasets are relative to action = 'delete' (delete PII data) and vary depending upon the identifier_type
# see the API documentation
# for MerakiPII.PIICalls module, you can call one or more seperated by a space
# as long as 1 or more datasets are valid for that identifier_type (e.g. mac takes the datasets: users loginAttempts)
datasets = 'users loginAttempts'

print('Submitting ' + '"' + action + '"' + ' request for ' '"' + identifier_type + '"' + ' with the value of '+ '"' + identifier_value + '"' + ': \n')

MyNewOrgPIIRequest = PIICalls.submitOrgPIIRequest(apikey, orgid, action, identifier_type, identifier_value, datasets=datasets)
print(json.dumps(MyNewOrgPIIRequest, indent=4, sort_keys=False))