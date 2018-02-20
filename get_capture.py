import argparse
from capture import *
from random import randint

parser = argparse.ArgumentParser(
    description="Check capture status")
parser.add_argument('job_id', help='The job_id to check status for')
args = parser.parse_args()

job_id = args.job_id

result = get_capture(job_id)
print(result)
