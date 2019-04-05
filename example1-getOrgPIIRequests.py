# simple example script that uses MerakiPII.PIICalls module to get all PII Requests for a given Organization
# A 404/null means the API call was successful but no PII call has been made for the network/org  
# PII delete and/or restrict processing examples start with example19-SubmitNewOrgDelRequest-MAC.py
# run those examples against a given network/org if you need data to return for this and other examples

# API Documentation for this call:  https://dashboard.meraki.com/api_docs#list-the-pii-requests-for-this-network-or-organization

# If you don't have a test environment, you can use DevNet Meraki Cloud Sandbox with a free account:
# https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

# see getOrgPIIRequests function in PIICalls module for details and arguments and below for other examples on assigning values

# next line imports PIICalls.py from the MerakiPII directory
from MerakiPII import PIICalls
# uncomment next line if you use EXAMPLE 4 below
#import configparser
#necessary for "pretty printing json in last 2 lines of this file"
import json

apikey = 'XXXXXXXXXXXXX'
orgid = 'XXXX'

MyOrgPIIRequests = PIICalls.getOrgPIIRequests(apikey, orgid,)
print('The following prints MyOrgPIIRequests: \n')
print(MyOrgPIIRequests)

### Many other ways to do the same thing ###

# EXAMPLE 2: 
#from MerakiPII import PIICalls
#apikey = 'XXXXXXXXXXXXX'
#orgid = 'XXXX'
#print(PIICalls.getOrgPIIRequests(apikey, orgid))

# EXAMPLE 3:
#from MerakiPII import PIICalls
#print(PIICalls.getOrgPIIRequests(apikey='XXXXXXXXXXXXX', orgid='XXXX'))

# EXAMPLE 4:
#from MerakiPII import PIICalls
#print(PIICalls.getOrgPIIRequests(XXXXXXXXXXXXX, XXXX))

# EXAMPLE 5: (don't forget to uncomment 'import config parser' above)
# 
# read API paramaters from config.ini file see https://docs.python.org/3/library/configparser.html
#config = configparser.ConfigParser()
#config.read('config.ini')
#apikey = config['MY-DEFAULT']['API_KEY']
#orgid = config['MY-DEFAULT']['ORG_ID']
#
# Call PIICalls.getOrgPIIRequests function and print out all PII Requests for a given org
#MyOrgPIIRequests = PIICalls.getOrgPIIRequests(apikey, orgid,)
#print('The following prints MyOrgPIIRequests: \n')
#print(MyOrgPIIRequests)

# add line breaks between calls
print('\n\n')

## if you want to print "cleanly" (i.e. in regular JSON format instead of Python list format)
# 
print('The following uses the Python json module to format and print the results of MyOrgPIIRequests: \n')
print(json.dumps(MyOrgPIIRequests, indent=4, sort_keys=False))