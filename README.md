# xepacketcap

This repo contains code to enable an API on Cisco IOS-XE devices for starting/stopping and transferring packet captures (pcap) files.  It requires the IOS-XE guestshell capability in order to function and has been tested extensively on the CSR 1000v platform.  In its current form, accepts an API call to create a packet job with arbitrary parameters and copy the resulting packet capture to an Amazon S3 bucket.

## Installation

Consider using this repo [here](https://github.com/chrishocker/iosxe-dev-env) to bring up a CSR for development purposes.  Otherwise, look at the Ansible playbook in that repo to see which steps are required to enable guestshell and configure NAT.  Once those pre-requisites are met, to install, clone the repo inside the guestshell on the IOS-XE device and install the requirements.

	[guestshell@guestshell ~]$ git clone https://github.com/chrishocker/xepacketcap.git
	[guestshell@guestshell ~]$ cd xepacketcap
	[guestshell@guestshell xepacketcap]$ sudo pip install -r requirements.txt

Then copy the xepacketcap.service file into the /etc/systemd/system directory and start it.

	[guestshell@guestshell xepacketcap]$ sudo cp xepacketcap.service /etc/systemd/system/
	[guestshell@guestshell xepacketcap]$ sudo systemctl enable xepacketcap
	[guestshell@guestshell xepacketcap]$ sudo systemctl start xepacketcap

Finally, in the IOS configuration of the device, configure an applet that runs the xepacketcap.py code at regular intervals.  This example checks for packet capture jobs every ten seconds.

	!
	event manager applet xepacketcap
	 event timer watchdog time 10 maxrun 360 ratelimit 10
	 action 1.0 cli command "enable"
	 action 2.0 cli command "guestshell run python xepacketcap/xepacketcap.py"
	!
	
Note, the maxrun and ratelimit arguments shown above are important.  The maxrun argument limits the total run time of the applet, which in our case needs to be large in order to accommodate larger packet capture durations.  The ratelimit argument won't allow more than instance of the applet to run in a given timeframe, which in our case should only be one every 10 seconds.

## Usage via Postman

To start a capture using Postman, make the following API call (replace the IP address with the address of your device):

	POST http://127.0.0.1:5000/pcap_json
	
Include the following JSON in the body of the request:

	{
		"iface": "g1",
		"proto": "tcp",
		"src": "any",
		"dst": "any",
		"bucket": "codefest-pcap",
		"duration": 10
	}

Where:

* *iface* is the interface to capture (e.g. GigabitEthernet1)
* *proto* is the procotol to capture (i.e. ip, tcp or udp)
* *src* is "any" or a host IP address
* *dst* is "any" or a host IP address
* *bucket* is the name of the AWS S3 bucket to upload to
* *duration* is the duration of the capture in seconds

This API call will return a JSON document with the job_id of the queued packet capture job.  You can check the status of the job with the folling API call:

	POST http://127.0.0.1:5000/status_json
	
Include the resulting job_id in the body of the request:

	{
		"job_id": 905928
	}

## Usage via Spark Bot

A seperate project to launch packet capture jobs via a Spark Bot utilizing this API can be found [here](https://github.com/zero2sixd/pcap-sparkbot).
## To do

* API security
* Packaging and distribution of packet capture app to IOS guestshell across multiple devices (eg. Ansible, Fog Director, etc.)

