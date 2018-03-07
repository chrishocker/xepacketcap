#!/usr/bin/env python
from capture import *
from time import sleep

'''A sqlite3 database named "capdb.db" is required to run this script. It must be located in the flash directory.
   Initialize the database with the following commands from the guestshell prompt:
   
         [guestshell@guestshell ~]$ cd /flash
         [guestshell@guestshell flash]$ sqlite3 capdb.db
         SQLite version 3.7.17 2013-05-20 00:56:22
         Enter ".help" for instructions
         Enter SQL statements terminated with a ";"
         sqlite> create table jobs(id integer primary key autoincrement, job_id int, iface text, proto text, src text, dst text, duration int, bucket text, filename text, url text, status text); 
         sqlite> .quit 
         [guestshell@guestshell flash]$  
'''

print('xepacketcap service started.')
print('waiting for jobs...')

process_jobs()