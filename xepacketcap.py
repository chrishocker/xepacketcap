#!/usr/bin/env python
import cli
import sys
# from csr_aws_guestshell import cag
import argparse
import time
<<<<<<< HEAD
from capture import *
=======
from capfilter import *
>>>>>>> 0c4170ca52a22e0bc7b9efe607112e356b0f205b

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
filename = args.filename
proto = args.protocol
src = args.src
dst = args.dst

<<<<<<< HEAD
start_capture(proto,src,dst)
=======
configuration = acl_command(proto,src,dst)
cli.configure(configuration)
cli.execute(
    "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
cmd = "monitor capture PKT_CAP interface %s both" % args.interface
cli.execute(cmd)
cli.execute("monitor capture PKT_CAP clear")
cli.execute("monitor capture PKT_CAP start")
>>>>>>> 0c4170ca52a22e0bc7b9efe607112e356b0f205b

for i in range(0, int(args.seconds)):
    time.sleep(1)
    sys.stdout.write("\r%d secs" % (i + 1))
    sys.stdout.flush()

print "\n"

<<<<<<< HEAD
cap_cleanup()

=======
cli.execute("monitor capture PKT_CAP stop")
cmd = "monitor capture PKT_CAP export location flash:%s" % filename # changed syntax to fit Cat9K
cli.execute(cmd)
configuration = 'no ip access-list extended PKT_CAP' # delete capture ACL so next capture has a fresh filter
cli.configure(configuration)
>>>>>>> 0c4170ca52a22e0bc7b9efe607112e356b0f205b

# cag().upload_file(bucket, filename)