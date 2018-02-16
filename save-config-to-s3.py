#!/usr/bin/env python
import sys
import cli
import argparse
import boto3


def upload_file(bucket, filename, directory="/bootflash/"):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(directory + filename, bucket, filename)
    except Exception as e:
        print "Uploading file Failed.  Error: %s" % (e)
        return False
    print "Upload Complete to S3 bucket %s" % (bucket)
    return True


parser = argparse.ArgumentParser(description="Upload config file")
parser.add_argument('bucket', help='The name of the bucket to upload to')
parser.add_argument('filename', help='Filename to upload to bucket')
args = parser.parse_args()

bucket = args.bucket
filename = args.filename

# first, save the config to bootflash
get_config = "copy running-config bootflash:%s" % filename
result = cli.execute(get_config)
if 'copied' not in result:
    print result
    sys.exit(1)

result = result.splitlines()

# print output of ios cli output showing the config copy
for line in result:
    if 'copied' in line:
        print line

upload_file(bucket, filename)
