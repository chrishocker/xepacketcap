import sqlite3
import time
from xepacketcap_db import *

def generate_filename():
    filename = str(int(time.time() * 1000)) + '.pcap'
    return filename

def add_capture(job_id, iface, proto, src, dst, duration, bucket):
    filename = generate_filename()
    url = 'https://s3-us-west-1.amazonaws.com/{}/{}'.format(bucket,filename)
    try:
        conn = create_connection()
        conn.execute(
           'INSERT into jobs (JOB_ID, IFACE, PROTO, SRC, DST, DURATION, BUCKET, FILENAME, URL, STATUS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
           (job_id, iface, proto, src, dst, duration, bucket, filename, url, 'WAITING'))
        conn.commit()
        print('job_id %d added to database with status WAITING' % job_id)
    except Exception as e:
        print(e)

def get_capture(job_id):
    try:
        conn = create_connection()
        conn.text_factory = str
        c = conn.cursor()
        c.execute('select * from jobs where job_id like (?)', (job_id,))
        job = c.fetchone()
        return job
    except Exception as e:
        print(e)

    return none

