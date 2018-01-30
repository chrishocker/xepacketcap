# xepacketcap

##High Level Tasks (in priority order)

* [Create a better dev environment](#dev-environment) (All)
* [Create the guestshell packet capture module in Python](#packet-capture-python-module) (Paul)
* [Define and create the API in Python Flask](#api) (Luis?)
* [Create the central control app](#central-control-app) (?)
* Extra credit:
	* API security
	* Packaging and distribution of packet capture app to IOS guestshell across multiple devices (eg. Ansible, Fog Director, etc.)

### Dev Environment
We need to find a way to simultaneously access the internet via laptop and push code to the Cat9K without copying and pasting into virtual desktops.  Consider switching to using CSR in CSN.

### Packet Capture Python Module
Develop packet capture Python module that can be run in IOS guestshell.  Implement functions for start, status and stop.

### API
Define API and develop in Python Flask.  API will be served via Flask running in guestshell.  API will consume start/status/stop functions provided by Python module above.

### Central Control App
Create a central control app that uses the APIs defined above to initial packet captures across multiple devices.  How this is to be done is TBD.  (Python? HTML?)