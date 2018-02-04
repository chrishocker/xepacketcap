#!/usr/bin/env python
import sys
# from csr_aws_guestshell import cag
import argparse
import time
from capture import *
import random


parser = argparse.ArgumentParser(
    description="Capture Packets and upload file to S3")
parser.add_argument('interface', help='The interface to capture from')
# parser.add_argument('bucket', help='The name of the bucket to upload to')
parser.add_argument('protocol', help='IP TCP UDP OSPF EIGRP ICMP')
parser.add_argument('src', help='x.x.x.x or any')
parser.add_argument('dst', help='x.x.x.x or any')
parser.add_argument('filename', help='Filename to upload to bucket')
parser.add_argument('--seconds', help='Seconds to capture', default=10)
args = parser.parse_args()

#bucket = args.bucket
duration = args.seconds
filename = args.filename
proto = args.protocol
src = args.src
dst = args.dst
jobID = random.randint(100000,999999)

cap_wait(jobID, duration)

start_capture(proto,src,dst)

for i in range(0, int(duration)):
    time.sleep(1)
    sys.stdout.write("\r%d secs" % (i + 1))
    sys.stdout.flush()

print "\n"


cap_cleanup()

# cag().upload_file(bucket, filename)