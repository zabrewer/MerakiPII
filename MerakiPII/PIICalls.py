#!/usr/bin/env python3
# coding=utf-8

"""
Cisco Meraki PII API Modules

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

Overview
This module is part of a project to assist with Meraki API calls specific to PII (personally identifiable information)
For specific details on the Meraki API PII calls, see the documentation:  https://dashboard.meraki.com/api_docs#pii

Dependencies
- Python 3.6
- 'requests' module
"""

__author__ = "Zach Brewer"
__email__ = "zbrewer@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import json
import re
import warnings

base_url = 'https://api.meraki.com/api/v0'

class Error(Exception):
    """

    Base module exception

    """
    pass


class ListLengthWarn(Warning):
    """

    Thrown when list lengths do not match

    """
    pass

class OrgPermissionError(Error):
    """

    Thrown when the API Key does not have access to supplied Organization ID

    """

    def __init__(self):
        self.default = 'Invalid Organization ID - Current API Key does not ' \
                       'have access to this Organization'

    def __str__(self):
        return repr(self.default)



def __isjson(myjson):
    """

    Args:
        myjson: String variable to be validated if it is JSON

    Returns: None

    """
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

def __hasorgaccess(apikey, targetorg):
    """

    Args:
        apikey: Meraki API Key to test access to the organization
        targetorg: Target organization to test access to for provided API Key

    Returns: None, raises OrgPermissionError if API Key does not have access to
    the specified Meraki Organization

    """
    geturl = '{0}/organizations'.format(str(base_url))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    dashboard = requests.get(geturl, headers=headers)
    currentorgs = json.loads(dashboard.text)
    orgs = []
    validjson = __isjson(dashboard.text)
    if validjson is True:
        for org in currentorgs:
            if int(org['id']) == int(targetorg):
                orgs.append(org['id'])
                return None
            else:
                pass
        raise OrgPermissionError
    return None

def __returnhandler(
        statuscode, returntext, objtype, suppressprint):
    """

    Args:
        statuscode: HTTP Status Code
        returntext: JSON String
        objtype: Type of object that operation was performed on
        (i.e. SSID, Network, Org, etc)
        suppressprint: Suppress any print output when function is called

    Returns:
        errmsg: If returntext JSON contains {'errors'} element
        returntext: If no error element, returns returntext

    """

    validreturn = __isjson(returntext)
    noerr = False
    errmesg = ''

    if validreturn:
        returntext = json.loads(returntext)

        try:
            errmesg = returntext['errors']
        except KeyError:
            noerr = True
        except TypeError:
            noerr = True

    if str(statuscode) == '200' and validreturn:
        if suppressprint is False:
            print('{0} Operation Successful - See returned data for results'
                  '\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '200':
        if suppressprint is False:
            print('{0} Operation Successful\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '201' and validreturn:
        if suppressprint is False:
            print('{0} Added Successfully - See returned data for results'
                  '\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '201':
        if suppressprint is False:
            print('{0} Added Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '204' and validreturn:
        if suppressprint is False:
            print('{0} Deleted Successfully - See returned data for results'
                  '\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '204':
        print('{0} Deleted Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '400' and validreturn and noerr is False:
        if suppressprint is False:
            print('Bad Request - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '400' and validreturn and noerr:
        if suppressprint is False:
            print('Bad Request - See returned data for details\n')
        return returntext
    elif str(statuscode) == '400':
        if suppressprint is False:
            print('Bad Request - No additional error data available\n')
    elif str(statuscode) == '401' and validreturn and noerr is False:
        if suppressprint is False:
            print('Unauthorized Access - See returned data '
                  'for error details\n')
        return errmesg
    elif str(statuscode) == '401' and validreturn:
        if suppressprint is False:
            print('Unauthorized Access')
        return returntext
    elif str(statuscode) == '404' and validreturn and noerr is False:
        if suppressprint is False:
            print('Resource Not Found - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '404' and validreturn:
        if suppressprint is False:
            print('Resource Not Found')
        return returntext
    elif str(statuscode) == '500':
        if suppressprint is False:
            print('HTTP 500 - Server Error')
        return returntext
    elif validreturn and noerr is False:
        if suppressprint is False:
            print('HTTP Status Code: {0} - See returned data for error details'
                  '\n'.format(str(statuscode)))
        return errmesg
    else:
        print('HTTP Status Code: {0} - No returned data'
              '\n'.format(str(statuscode)))


#####################################

# FOR ORG, List the keys required to access Personally Identifiable Information (PII) for a given identifier. 
# Exactly one identifier will be accepted. (username, email, mac, serial, imei, bluetoothMac)
# If the organization contains org-wide Systems Manager users matching the key provided then there will
# be an entry with the key "0" containing the applicable keys.
# https://dashboard.meraki.com/api_docs#list-the-keys-required-to-access-personally-identifiable-information-pii-for-a-given-identifier
def getOrgPIIKeys(apikey, orgid, identifier_type, identifier, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'PII'

    geturl = '{0}/organizations/{1}/pii/piiKeys?{2}={3}'.format(
        str(base_url), str(orgid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, List the keys required to access Personally Identifiable Information (PII) for a given identifier. 
# Exactly one identifier will be accepted. (username, email, mac, serial, imei, bluetoothMac)
# If the organization contains org-wide Systems Manager users matching the key provided then there will
# be an entry with the key "0" containing the applicable keys.
# https://dashboard.meraki.com/api_docs#list-the-keys-required-to-access-personally-identifiable-information-pii-for-a-given-identifier
def getNetworkPIIKeys(apikey, networkid, identifier_type, identifier, suppressprint=False):
    calltype = 'PII'
    geturl = '{0}/networks/{1}/pii/piiKeys?{2}={3}'.format(
        str(base_url), str(networkid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For ORG, Given a piece of Personally Identifiable Information (PII), 
# return the Systems Manager device ID(s) associated with that identifier. 
# These device IDs can be used with the Systems Manager API endpoints to
# retrieve device details. Exactly one identifier will be accepted.
# (username, email, mac, serial, imei, bluetoothMac)
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-device-ids-associated-with-that-identifier
def getOrgSMDevicesForKey(apikey, orgid, identifier_type, identifier, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'PII'

    geturl = '{0}/organizations/{1}/pii/smDevicesForKey?{2}={3}'.format(
        str(base_url), str(orgid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, Given a piece of Personally Identifiable Information (PII), 
# return the Systems Manager device ID(s) associated with that identifier. 
# These device IDs can be used with the Systems Manager API endpoints to
# retrieve device details. Exactly one identifier will be accepted.
# (username, email, mac, serial, imei, bluetoothMac)
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-device-ids-associated-with-that-identifier
def getNetworkSMDevicesForKey(apikey, networkid, identifier_type, identifier, suppressprint=False):
    calltype = 'PII'
    geturl = '{0}/networks/{1}/pii/smDevicesForKey?{2}={3}'.format(
        str(base_url), str(networkid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


# For ORG, Given a piece of Personally Identifiable Information (PII), 
# return the Systems Manager owner ID(s) associated with that identifier. 
# These owner IDs can be used with the Systems Manager API endpoints to
# retrieve owner details. Exactly one identifier will be accepted.
# (username, email, mac, serial, imei, bluetoothMac)
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-device-ids-associated-with-that-identifier
def getOrgSMOwnersForKey(apikey, orgid, identifier_type, identifier, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'PII'

    geturl = '{0}/organizations/{1}/pii/smOwnersForKey?{2}={3}'.format(
        str(base_url), str(orgid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, Given a piece of Personally Identifiable Information (PII), 
# return the Systems Manager owner ID(s) associated with that identifier. 
# These owner IDs can be used with the Systems Manager API endpoints to
# retrieve device details. Exactly one identifier will be accepted.
# (username, email, mac, serial, imei, bluetoothMac)
# https://dashboard.meraki.com/api_docs#given-a-piece-of-personally-identifiable-information-pii-return-the-systems-manager-device-ids-associated-with-that-identifier
def getNetworkSMOwnersForKey(apikey, networkid, identifier_type, identifier, suppressprint=False):
    calltype = 'PII'
    geturl = '{0}/networks/{1}/pii/smOwnersForKey?{2}={3}'.format(
        str(base_url), str(networkid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For ORG, list the PII requests for given ORG
# (Do not confuse with getOrgPIIRequest which gives details about a SINGLE request)
# https://dashboard.meraki.com/api_docs#list-the-pii-requests-for-this-network-or-organization
def getOrgPIIRequests(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'PII'

    geturl = '{0}/organizations/{1}/pii/requests'.format(
        str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, list the PII requests for given network
# (Do not confuse with getNetworkPIIRequest which gives details about a SINGLE request)
# https://dashboard.meraki.com/api_docs#list-the-pii-requests-for-this-network-or-organization
def getNetworkPIIRequests(apikey, networkid, suppressprint=False):
    calltype = 'PII'
    geturl = '{0}/networks/{1}/pii/requests'.format(
        str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For ORG, give details about a SINGLE PII request
# NOTE:  requires individual request ID which can be retrieved from getOrgPIIRequests or getNetworkPIIRequests
# (Do not confuse with getOrgPIIRequests which lists ALL requests for a given Org)
# https://dashboard.meraki.com/api_docs#return-a-pii-request
def getOrgPIIRequest(apikey, orgid, requestid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'PII'

    geturl = '{0}/organizations/{1}/pii/requests/{2}'.format(
        str(base_url), str(orgid), str(requestid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, give details about a SINGLE PII request
# NOTE:  requires individual request ID which can be retrieved from getOrgPIIRequests or getNetworkPIIRequests
# (Do not confuse with getNetworkPIIRequests which lists ALL requests for a given Network)
# https://dashboard.meraki.com/api_docs#return-a-pii-request
def getNetworkPIIRequest(apikey, networkid, requestid, suppressprint=False):
    calltype = 'PII'
    geturl = '{0}/networks/{1}/pii/requests/{2}'.format(
        str(base_url), str(networkid), str(requestid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For ORG, Submit a new ORG level delete or restrict processing PII request
# https://dashboard.meraki.com/api_docs#submit-a-new-delete-or-restrict-processing-pii-request
def submitOrgPIIRequest(apikey, orgid, action, identifier_type, identifier, datasets=None, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)

    calltype = 'PII'
    puturl = '{0}/organizations/{1}/pii/requests'.format(
    str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}
    # meraki api expects type: delete or restrict processing
    # for restrict processing, only certain paramaters (identifer_types) are allowed
    # we are checking for these types and adding their values to our dict if defined
    if action == 'restrict processing':
        putdata['datasets'] = 'all'
        #putdata['type'] = 'restrict processing'
        if identifier_type == 'mac':
            #print(mac)
            putdata['mac'] = identifier 
        elif identifier_type == 'smDeviceID':
            putdata['smDeviceId'] = identifier
        elif identifier_type == 'smUserID':
            putdata['smUserID'] = identifier
        else:
            print('Valid API identifer types (paramaters) for restrict processing are "mac", "smDeviceId", or "smUserId"')

    elif action == 'delete':
        #take SPACE separated dataset and checks if each are valid for given PII type
        splitdata = datasets.split(' ')
        # FYI, 'not in' used to utilize python ANY (i.e. any valid combination of datasets for given PII key)
        # probably a better way to do this, may re-write
        inValidMacDataset = any(
            data not in ('usage', 'events', 'traffic', 'all')
            for data in splitdata
        )
        inValidEmailDataset = any(
            data not in ('users', 'loginAttempts')
            for data in splitdata
        )
        inValidUsernameDataset = any(
            data not in ('users', 'loginAttempts', 'all')
            for data in splitdata
        )
        inValidBluetoothMacDataset = any(
            data not in ('client', 'connectivity', 'all')
            for data in splitdata
        )
        inValidsmDeviceIdDataset = any(
            data not in ('device', 'all')
            for data in splitdata
        )
        inValidsmUserIdDataset = any(
            data not in ('user', 'all')
            for data in splitdata
        )
        # begin checks of type and possible datasets to send to API via PUT
        if identifier_type == 'mac':
            if inValidMacDataset:
                print('\nValid datasets for PII type mac must be dataset "all" OR one or more ' + 
                'of the following (separated by a space): \n\n' +
                'usage traffic events \n')
                return None
            else:
                putdata['mac'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['mac'], putdata['datasets'])

        elif identifier_type == 'email':
            if inValidEmailDataset:
                print('\nValid datasets for PII type email must be dataset one or more ' 
                'of the following (separated by a space): \n\n'
                'users loginAttempts \n')
                return None
            else:
                putdata['email'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['email'], putdata['datasets'])

        elif identifier_type == 'username':
            if inValidUsernameDataset:
                print('\nValid datasets for PII type username must be dataset "all" OR one or more ' 
                'of the following (separated by a space): \n\n'
                'users loginAttempts \n')
                return None      
            else:
                putdata['username'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['username'], putdata['datasets'])

        elif identifier_type == 'bluetoothMac':
            if inValidBluetoothMacDataset:
                print('\nValid datasets for PII type buletoothMac must be dataset "all" OR one or more ' 
                'of the following (separated by a space): \n\n'
                'users loginAttempts \n')
                return None
            else:
                putdata['bluetoothMac'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['bluetoothMac'], putdata['datasets'])

        elif identifier_type == 'smDeviceID':
            if inValidsmDeviceIDDataset:
                print('Valid dataset(s) for PII type smDeviceID must either be "all" or "device"')
            else:
                putdata['smDeviceID'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['smDeviceID'], putdata['datasets'])

        elif identifier_type == 'smUserID':
            if inValidsmUserIDDataset:
                print('Valid dataset(s) for PII type smDeviceID must either be "all" or "user"')
            else:
                putdata['smDeviceID'] = identifier
                putdata['datasets'] = splitdata
                #print(putdata['smDeviceID'], putdata['datasets'])
        
        else:
            print('identifier_type can only be ONE of the following: '
                '"mac", "email", "username", "bluetoothMac", "smDeviceId", "smUserId"')
            return None
        
    else:
        print('Action can only be one of "restrict processing" or "delete"')
        return None

    putdata['type'] = action

    data=json.dumps(putdata) 
    dashboard = requests.post(puturl, data=json.dumps(putdata), headers=headers)
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, Submit a new network level delete or restrict processing PII request
# https://dashboard.meraki.com/api_docs#submit-a-new-delete-or-restrict-processing-pii-request
def submitNetworkPIIRequest(apikey, networkid, action, identifier_type, identifier, email=None, datasets=None, username=None, mac=None, smDeviceID=None, smUserID=None, bluetoothMac=None, suppressprint=False):
    calltype = 'PII'
    puturl = '{0}/networks/{1}/pii/requests?{2}={3}'.format(
        str(base_url), str(networkid), str(identifier_type), str(identifier))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = {}
    # meraki api expects type: delete or restrict processing
    # type is a reserved word in Python so this line is slightly different than others
    print(action)
    if action == 'restrict processing':
        putdata['datasets'] = 'all'
        #putdata['type'] = 'restrict processing'
        if mac is not None:
            print(mac)
            putdata['mac'] = mac 
        elif smDeviceID is not None:
            putdata['smDeviceId'] = smDeviceID
        elif smUserID is not None:
            putdata['smUserID'] = smUserID
        else:
            print('Valid API paramaters for restrict processing are "mac", "smDeviceId", or "smUserId"')
         
    elif action == 'delete':
        splitdata = datasets.split(' ')
        #take SPACE separated dataset and checks if each are valid for given PII type
        # FYI, 'not in' used to utilize python ANY
        inValidMacDataset = any(
            data not in ('usage', 'events', 'traffic', 'all')
            for data in splitdata
        )
        inValidEmailDataset = any(
            data not in ('users', 'loginAttempts', 'all')
            for data in splitdata
        )
        inValidUsernameDataset = any(
            data not in ('users', 'loginAttempts', 'all')
            for data in splitdata
        )
        inValidBluetoothMacDataset = any(
            data not in ('client', 'connectivity', 'all')
            for data in splitdata
        )
        inValidsmDeviceIdDataset = any(
            data not in ('device', 'all')
            for data in splitdata
        )
        inValidsmUserIdDataset = any(
            data not in ('user', 'all')
            for data in splitdata
        )
        # begin checks of type and possible datasets to send to API via PUT
        if mac is not None:
            if inValidMacDataset:
                print('\nValid datasets for PII type mac must be dataset "all" OR one or more ' + 
                'of the following (separated by a space): \n\n' +
                'usage traffic events \n')
                return None
            else:
                putdata['mac'] = mac
                putdata['datasets'] = splitdata
                print(putdata['mac'], putdata['datasets'])

        if email is not None:
            if inValidEmailDataset:
                print('\nValid datasets for PII type email must be dataset "all" OR one or more ' + 
                'of the following (separated by a space): \n\n' +
                'users loginAttempts \n')
                return None
            else:
                putdata['email'] = email
                putdata['datasets'] = splitdata
                print(putdata['email'], putdata['datasets'])

        if username is not None:
            if inValidUsernameDataset:
                print('\nValid datasets for PII type username must be dataset "all" OR one or more ' + 
                'of the following (separated by a space): \n\n' +
                'users loginAttempts \n')
                return None      
            else:
                putdata['username'] = username
                putdata['datasets'] = splitdata
                print(putdata['username'], putdata['datasets'])

        if bluetoothMac is not None:
            if inValidBluetoothMacDataset:
                print('\nValid datasets for PII type buletoothMac must be dataset "all" OR one or more ' + 
                'of the following (separated by a space): \n\n' +
                'users loginAttempts \n')
                return None
            else:
                putdata['bluetoothMac'] = bluetoothMac
                putdata['datasets'] = splitdata
                print(putdata['bluetoothMac'], putdata['datasets'])

        if smDeviceID is not None:
            if inValidsmDeviceIDDataset:
                print('Valid dataset(s) for PII type smDeviceID must either be "all" or "device"')
            else:
                putdata['smDeviceID'] = smDeviceID
                putdata['datasets'] = splitdata
                print(putdata['smDeviceID'], putdata['datasets'])

        if smUserID is not None:
            if inValidsmUserIDDataset:
                print('Valid dataset(s) for PII type smDeviceID must either be "all" or "user"')
            else:
                putdata['smDeviceID'] = smDeviceID
                putdata['datasets'] = splitdata
                print(putdata['smDeviceID'], putdata['datasets'])
        
    else:
        print('Action can only be one of "restrict processing" or "delete"')
        return None

    putdata['type'] = action

    data=json.dumps(putdata) 
    dashboard = requests.post(puturl, data=json.dumps(putdata), headers=headers)
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


# For ORG, delete an existing PII restrict processing request
# NOTE:  Requires an existing PII restrict processing requestID from either getOrgPIIRequests or getNetworkPIIRequests
# https://dashboard.meraki.com/api_docs#delete-a-restrict-processing-pii-request
def delOrgPIIRequest(apikey, orgid, requestid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    
    calltype = 'PII'
    delurl = '{0}/organizations/{1}/pii/requests/{2}'.format(
        str(base_url), str(orgid), str(requestid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    print(delurl)
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result

# For NETWORK, delete an existing PII restrict processing request
# NOTE:  Requires an existing PII restrict processing requestID from either getOrgPIIRequests or getNetworkPIIRequests
# https://dashboard.meraki.com/api_docs#delete-a-restrict-processing-pii-request
def delNetworkPIIRequest(apikey, orgid, requestid, suppressprint=False):

    calltype = 'PII'
    delurl = '{0}/networks/{1}/pii/requests'.format(
        str(base_url), str(networkid), str(requestid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(
        dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result