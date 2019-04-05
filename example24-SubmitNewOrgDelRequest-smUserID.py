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
# username usually applies only to a WIFI network with a splash page and local (Meraki) auth
# basically sending a DELETE PII request to a WIFI network/org will remove
#  user's username and other data under WIRELESS --> SPLASH LOGINS  in the Meraki Dashboard
config = configparser.ConfigParser()
config.read('config.ini')
# use MDM section of config.ini as these are MDM/SM specific PII calls
apikey = config['DEFAULT-KEYS-MDM']['API_KEY']
orgid = config['DEFAULT-KEYS-MDM']['ORG_ID']
# set "action" argument directly rather than read from config.ini
action = 'delete'
# set IDENTIFIER_TYPE to smUser as defined in config.ini
identifier_type = config['DELETE-AND-RESTRICT-DATA']['IDENTIFIER_TYPE_SMUSER']
# set IDENTIFIER to an actual smUser value in config.ini
identifier_value = config['DELETE-AND-RESTRICT-DATA']['IDENTIFIER_VALUE_SMUSER']
# datasets are relative to action = 'delete' (delete PII data) and vary depending upon the identifier_type
# see the API documentation
# for MerakiPII.PIICalls module, you can call one or more seperated by a space
# as long as 1 or more datasets are valid for that identifier_type (e.g. username takes the datasets: users loginAttempts)
datasets = 'user'

# we use identifier_type=identifer_type and other assignments when calling PIICalls.submitOrgPIIRequest
# this sets optional arguments in the PIICalls.submitOrgPIIRequest function to those defined here.
# i.e. submitORGPIIRequest_ARGUMENT = ARGUMENT_defined_in_this_python_file
# if we don't, the arguments get passed in postionally and you may have an issue such as mac address value passed as an username
# argument into the function and subsequent Meraki API call.
MyNewOrgPIIRequest = PIICalls.submitOrgPIIRequest(apikey, orgid, action, identifier_type, identifier_value, datasets=datasets)
print('Submitting ' + '"' + action + '"' + ' request for ' '"' + identifier_type + '"' + ' with the value of '+ '"' + identifier_value + '"' + ': \n')
print(json.dumps(MyNewOrgPIIRequest, indent=4, sort_keys=False))