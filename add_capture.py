import argparse
from capture import *
from random import randint

parser = argparse.ArgumentParser(
    description="Capture Packets and upload file to S3")
parser.add_argument('interface', help='The interface to capture from')
parser.add_argument('protocol', help='IP TCP UDP OSPF EIGRP ICMP')
parser.add_argument('src', help='x.x.x.x or any')
parser.add_argument('dst', help='x.x.x.x or any')
parser.add_argument('bucket', help='The name of the bucket to upload to')
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
job_id = randint(100000,999999)


add_capture(job_id,iface,proto,src,dst,duration,bucket,filename)
