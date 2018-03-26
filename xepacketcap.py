#!/usr/bin/env python 
from xepacketcap_core import *
from time import sleep
#import sys

sql_create_jobs_table = """ CREATE TABLE IF NOT EXISTS jobs (
                                        id integer PRIMARY KEY autoincrement,
                                        job_id int,
                                        iface text,
                                        proto text,
                                        src text,
                                        dst text,
                                        duration int,
                                        bucket text,
                                        filename text,
                                        url text,
                                        status text
                                    ); """
# flush stdout immediately for logging to a file
#sys.stdout.flush()

#print('xepacketcap service started.')
print('checking for jobs...')

conn = create_connection()
create_table(conn, sql_create_jobs_table)
process_job()
