# functions to set up, start, and stop packet capture in XE device
# note - may need to change syntax of export command for CSR

import cli
import sys
import sqlite3
import time
import boto3
#from random import randint

def acl_command(proto,src,dst):
    if (src == 'any') and (dst == 'any'):
        command = '''ip access-list extended PKT_CAP
                     permit %s %s %s''' %(proto,src,dst)
    elif (src == 'any') and (dst != 'any'):
        command = '''ip access-list extended PKT_CAP
                     permit %s %s host %s''' %(proto,src,dst)
    elif (src != 'any') and (dst == 'any'):
        command = '''ip access-list extended PKT_CAP
                     permit %s host %s %s''' %(proto,src,dst)
    else:
        command = '''ip access-list extended PKT_CAP
                     permit %s host %s host %s''' %(proto,src,dst)
    return command


def cap_wait(jobID,duration):
    #determine whether we need to wait for other jobs to finish
    #calculate the number of rows in the jobs database, assign to int(numrows)
    #jobID = randint(100000, 999999)
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    c.execute('select count(*) from jobs where status not like "COMPLETE"')
    rows = c.fetchone()
    numrows = rows[0]

    if numrows == 0:
        # if there are no jobs in the database, add my job to database and GO!!!!
        add_job_status_inprogress(jobID, duration)
        wait = 0
    else:
        #calculate wait time based on duration of jobs already in queue
        c.execute('select duration from jobs where status not like "COMPLETE"')
        output = c.fetchall()
        output = [i[0] for i in output] #convert list of tuples to list of ints
        wait = 10 # add 10 second buffer to wait time
        for i in range(len(output)):
            wait = wait + output[i]
            #add my job to capdb
        add_job_status_waiting(jobID, duration)
        waitstr = str(wait)
        print 'Other jobs are in the queue. Your capture starts in ' + waitstr + ' seconds.'
        # begin wait counter
        for i in range(0, wait):
            time.sleep(1)
            sys.stdout.write("\r%d secs" % (i + 1))
            sys.stdout.flush()
        # when wait time completes, proceed with capture
    return wait #, jobID


def start_capture(iface,proto,src,dst,jobID,wait,duration):
    configuration = acl_command(proto, src, dst)
    #print configuration
    print '\n'
    cli.configure(configuration)
    cli.execute(
        "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
    cmd = "monitor capture PKT_CAP interface %s both" % iface
    cli.execute(cmd)
    cli.execute("monitor capture PKT_CAP clear")
    print 'Your capture is starting...'
    print 'Job ID = {}'.format(jobID)
    print '\n'
    if wait == 0:
        cli.execute("monitor capture PKT_CAP start")
        display_countdown(duration)
    else:
        update_status_inprogress(jobID)
        cli.execute("monitor capture PKT_CAP start")
        display_countdown(duration)


def cap_cleanup(jobID,bucket,filename):
    cli.execute("monitor capture PKT_CAP stop")
    cmd = "monitor capture PKT_CAP export flash:%s" % filename
    cli.execute(cmd)
    configuration = 'no ip access-list extended PKT_CAP'  # delete capture ACL so next capture has a fresh filter
    cli.configure(configuration)
    upload_file(bucket,filename,jobID)
    update_status_complete(bucket,filename,jobID)


def add_job_status_inprogress(jobID,duration):
    conn = sqlite3.connect('capdb.db')
    conn.execute('INSERT into jobs (JOB_ID, DURATION, STATUS) VALUES (?, ?, ?)', (jobID, duration, 'INPROGRESS'))
    conn.commit()
    conn.close()


def add_job_status_waiting(jobID,duration):
    conn = sqlite3.connect('capdb.db')
    conn.execute('INSERT into jobs (JOB_ID, DURATION, STATUS) VALUES (?, ?, ?)', (jobID, duration, 'WAITING'))
    conn.commit()
    conn.close()


def update_status_complete(bucket,filename,jobID):
    URL = 'https://s3-us-west-1.amazonaws.com/{}/{}'.format(bucket,filename)
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    c.execute('UPDATE jobs set URL = (?) where JOB_ID = (?)', (URL, jobID))
    c.execute('UPDATE jobs set status = "COMPLETE" where JOB_ID = (?)', (jobID,))
    conn.commit()
    conn.close()


def update_status_inprogress(jobID):
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    c.execute('UPDATE jobs set status = "INPROGRESS" where JOB_ID = (?)', (jobID,))
    conn.commit()
    conn.close()


def update_status_uploading(jobID):
    conn = sqlite3.connect('capdb.db')
    c = conn.cursor()
    c.execute('UPDATE jobs set status = "UPLOADING" where JOB_ID = (?)', (jobID,))
    conn.commit()
    conn.close()


def display_countdown(duration):
    for i in range(0, int(duration)):
        time.sleep(1)
        sys.stdout.write("\r%d secs" % (i + 1))
        sys.stdout.flush()


def upload_file(bucket,filename,jobID,directory="/bootflash/"):
    s3_client = boto3.client('s3')
    update_status_uploading(jobID)
    try:
        s3_client.upload_file(directory + filename, bucket, filename)
    except Exception as e:
        print "Uploading file Failed.  Error: %s" % (e)
        return False
    print "Upload Complete to S3 bucket %s" % (bucket)
    return True


