import cli
import sys
import sqlite3
import time
import boto3

# for simplicity, keep the database in memory
db_file = '/var/tmp/capdb.db'

def create_connection():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return none

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

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

def start_capture(job_id, iface, proto, src, dst):
    configuration = acl_command(proto, src, dst)
    cli.configure(configuration)
    cli.execute(
        "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
    cmd = "monitor capture PKT_CAP interface %s both" % iface
    cli.execute(cmd)
    cli.execute("monitor capture PKT_CAP clear")
    print('job_id %d starting' % job_id)
    cli.execute("monitor capture PKT_CAP start")

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

def stop_capture(job_id, filename):
    cli.execute("monitor capture PKT_CAP stop")
    cmd = "monitor capture PKT_CAP export flash:%s" % filename
    cli.execute(cmd)
    configuration = 'no ip access-list extended PKT_CAP'  # delete capture ACL so next capture has a fresh filter
    cli.configure(configuration)
    print('job_id %d stopped' % job_id)
    #upload_file(bucket,filename,job_id)

def delete_capture(filename):
    cmd = "delete flash:%s" % filename
    cli.execute(cmd)

def update_status(job_id, status):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('UPDATE jobs set status = (?) where JOB_ID = (?)', (status, job_id,))
        conn.commit()
        print('job_id %d status changed to %s' % (job_id, status))
    except Exception as e:
        print(e)

def upload_capture(job_id, bucket,filename,directory="/bootflash/"):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(directory + filename, bucket, filename)
    except Exception as e:
        print('job_id %d upload failed: %s' % (job_id, e))
        return False
    print('job_id %d upload complete to S3 bucket %s' % (job_id, bucket))

    return True

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

def generate_filename():
    #result = cli.execute("show run | inc hostname")
    #print(result)
    #output = result.split()
    #print(output)
    #hostname = output[1]
    #filename = hostname + '-' + str(int(time.time() * 1000))
    filename = str(int(time.time() * 1000)) + '.pcap'
    return filename
    
def process_jobs():
    while True:
        conn = create_connection()
        try:
            c = conn.cursor()
            c.execute('select * from jobs where status like "WAITING" limit 1')
            job = c.fetchone()
            if job:
                try:
                    id, job_id, iface, proto, src, dst, duration, bucket, filename, url, status = job
                    start_capture(job_id, iface, proto, src, dst)
                    update_status(job_id, 'STARTED')
                    time.sleep(duration)
                    stop_capture(job_id, filename)
                    update_status(job_id, 'STOPPED')
                    update_status(job_id, 'UPLOADING')
                    if upload_capture(job_id, bucket, filename):
                        update_status(job_id, 'UPLOADED')
                    else:
                        update_status(job_id, 'ERROR')
                except Exception as (e):
                    print(e)
                    update_status(job_id, 'ERROR')
        except Exception as (e):
            print(e)
        finally:
            time.sleep(10)

def process_job():
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('select * from jobs where status like "WAITING" limit 1')
        job = c.fetchone()
    except Exception as (e):
        print(e)
    if job:
        try:
            id, job_id, iface, proto, src, dst, duration, bucket, filename, url, status = job
            start_capture(job_id, iface, proto, src, dst)
            update_status(job_id, 'STARTED')
            time.sleep(duration)
            stop_capture(job_id, filename)
            update_status(job_id, 'STOPPED')
            update_status(job_id, 'UPLOADING')
            if upload_capture(job_id, bucket, filename):
                update_status(job_id, 'UPLOADED')
            else:
                update_status(job_id, 'ERROR')
            delete_capture(filename)
        except Exception as (e):
            print(e)
            update_status(job_id, 'ERROR')

