#!/usr/bin/env python
# from csr_aws_guestshell import cag
import argparse
from capture import *
from random import randint

'''A sqlite3 database named "capdb.db" is required to run this script. It must be located in the flash directory.
   Initialize the database with the following commands from the guestshell prompt:
   
         [guestshell@guestshell ~]$ cd /flash
         [guestshell@guestshell flash]$ sqlite3 capdb.db
         SQLite version 3.7.17 2013-05-20 00:56:22
         Enter ".help" for instructions
         Enter SQL statements terminated with a ";"
         sqlite> create table jobs(id integer primary key autoincrement, job_id int,\ 
                                   duration int, status text, URL text);
         sqlite> .quit 
         [guestshell@guestshell flash]$  
'''


parser = argparse.ArgumentParser(
    description="Capture Packets and upload file to S3")
parser.add_argument('interface', help='The interface to capture from')
parser.add_argument('bucket', help='The name of the bucket to upload to')
parser.add_argument('protocol', help='IP TCP UDP OSPF EIGRP ICMP')
parser.add_argument('src', help='x.x.x.x or any')
parser.add_argument('dst', help='x.x.x.x or any')
parser.add_argument('filename', help='Filename to upload to bucket')
parser.add_argument('--seconds', help='Seconds to capture', default=10)
args = parser.parse_args()

bucket = args.bucket
duration = args.seconds
iface = args.interface
filename = args.filename
proto = args.protocol
src = args.src
dst = args.dst
jobID = randint(100000,999999)
jobIDstr = str(jobID)

print 'Job ID = ' + jobIDstr
print '\n'
wait = cap_wait(jobID, duration)

'''
waitAndJobID = capwait(duration)
wait = waitAndJobID[0]
jobID = waitAndJobID[1]
'''

start_capture(iface,proto,src,dst,jobID,wait,duration)

print "\n"

cap_cleanup(jobID,bucket,filename)

# upload_file(bucket,filename)
