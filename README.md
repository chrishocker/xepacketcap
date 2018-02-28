# xepacketcap

Use the following steps to set up the environment and run the script.
Note: GuestShell must be enabled and configured to talk to the world. 

STEP 1 - Install PIP

    sudo yum -y install pip


STEP 2 - Install Flask & Flask Alchemy

    sudo pip install flask
    sudo pip install flask_sqlAlchemy


STEP 3 - Install AWSCLI & Boto3

    sudo pip install awscli
    sudo pip install boto3

STEP 4 - Clone Repo

    git clone https://github.com/chrishocker/xepacketcap.git

STEP 5 - Set up database 

    Issue the following commands from the repo directory:
   
         [guestshell@guestshell xepacketcap]$ sqlite3 capdb.db
         SQLite version 3.7.17 2013-05-20 00:56:22
         Enter ".help" for instructions
         Enter SQL statements terminated with a ";"
         sqlite> create table jobs(id integer primary key autoincrement, job_id int, iface text, proto text, src text, dst text, duration int, bucket text, filename text, url text, status text); 
         sqlite> .quit 
         [guestshell@guestshell flash]$  

STEP 6 - Enable the API script and Packet Capture Daemon

    From the repo directory, run the following commands:

	    python pcap_api.py
	    python xepacketcap.py

Now you are ready to run packet capture jobs using the XE Packet Capture App using Sparkbot, Web Interface, Postman or CLI.

From the CLI, run the following command (arguments are flexible):

        python add_capture.py --seconds 10 gi1 ip any any codefest-pcap



