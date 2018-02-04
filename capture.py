# functions to set up, start, and stop packet capture in XE device
# note - may need to change syntax of export command for CSR

import cli
import subprocess
import sys
import sqlite3
import time


def acl_command(proto,src,dst):
    if (src == 'any') and (dst == 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s %s %s''' %(proto,src,dst)
    elif (src == 'any') and (dst != 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s %s host %s''' %(proto,src,dst)
    elif (src != 'any') and (dst != 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s host %s %s''' %(proto,src,dst)
    else:
        command = '''ip access-list extended PKT_CAP
                           permit %s host %s host %s''' %(proto,src,dst)

    return command


def start_capture(proto,src,dst):
    configuration = acl_command(proto, src, dst)
    cli.configure(configuration)
    cli.execute(
        "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
    cmd = "monitor capture PKT_CAP interface %s both" % args.interface
    cli.execute(cmd)
    cli.execute("monitor capture PKT_CAP clear")
    cli.execute("monitor capture PKT_CAP start")


def cap_cleanup(jobID):
    cli.execute("monitor capture PKT_CAP stop")
    cmd = "monitor capture PKT_CAP export location flash:%s" % filename  # changed syntax to fit Cat9K
    cli.execute(cmd)
    configuration = 'no ip access-list extended PKT_CAP'  # delete capture ACL so next capture has a fresh filter
    cli.configure(configuration)
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    c.execute('DELETE from CAPJOBS where JOB_ID = %d', (jobID))
    conn.commit()
    conn.close()


def cap_check():
    output = subprocess.check_output('ps -ef | grep xepacketcap.py', shell=True)
    parts = output.split(' ')
    if '/flash/xepacketcap.py' in parts:
        print 'Capture underway, try again later'
        sys.exit()
    else:
        pass

def cap_wait(jobID,duration):
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    count = c.execute('select count(*) from jobs;')
    rows = c.fetchone()
    numrows = rows[0]
    if numrows == 0:
        break # if there are no jobs in the queue, GO!!!!
    else:
        #calculate wait time based on duration of jobs already in queue
        c.execute('select duration from jobs')
        output = c.fetchall()
        wait = 10 # add 10 second buffer to wait time
        for i in output:
            wait = wait + output[i][0]
        #add my job to capdb
        conn.execute('INSERT INTO CAPJOBS (JOBID, DURATION) VALUES' (%d, %d)', (jobID, duration))
        conn.commit()
        conn.close()
        #begin wait counter
        for i in range(0, wait):
            time.sleep(1)
            '''sys.stdout.write("\r%d secs" % (i + 1))
               sys.stdout.flush()'''
        # when wait time completes, proceed with capture
        # future enhancement: check db again to verify I'm at the top of the list, if yes then go ahead






