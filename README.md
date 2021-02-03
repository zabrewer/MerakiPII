##  Description

Meraki PII is a Python package used to interact with the Meraki Dashboard API for Personally Identifiable Information (PII).

The official documentation for PII related API calls can be found [here](https://dashboard.meraki.com/api_docs#pii).

##  Dependencies and Requirements
Tested on Python 3.7 and Requests 2.21.0

##  Installation

Preferred method of installation is in a Python virtual environment.

1) Clone the project
```
git clone https://github.com/zabrewer/MerakiPII
```

2) create venv in same directory:
```
python3 -m venv MerakiPII/
```

3) activate venv and download dependencies
```
cd MerakiPII/
source bin/activate
```

4) satisfy dependencies
```
pip install requests
```

##   Use
Review PII related functions in the MerakiPII/PII.py package or review the individual example Python files for basic use.  

All example python files point to a file named config.ini for Meraki Dashboard API Keys, Meraki Org, and other required parameters.  See example-config.ini. 

##  Further PII and GDPR related documentation

[Meraki Data Privacy and Protection Features](https://documentation.meraki.com/zGeneral_Administration/Privacy_and_Security/Meraki_Data_Privacy_and_Protection_Features)

[EU Cloud Configuration Guide](https://documentation.meraki.com/zGeneral_Administration/Privacy_and_Security/EU_Cloud_Configuration_Guide)

##  Credit

[shiyuechengineer](https://github.com/shiyuechengineer) wrote the error functions and non-PII functions.  I made use of the same in order to merge this project into [the official meraki-dashboard Python module](https://github.com/shiyuechengineer/meraki-dashboard) which does not currently contain PII API calls. 

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
