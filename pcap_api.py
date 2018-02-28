from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from capture import *
from threading import Thread
from random import randint


app = Flask(__name__)

@app.route('/pcap', methods=['GET', 'POST']) #allow both GET and POST requests
def run_pcap():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        job_id = randint(100000,999999)
        iface = request.form['iface']
        proto = request.form['proto']
        src = request.form['src']
        dst = request.form['dst']
        duration = request.form['duration']
        bucket = request.form['bucket']
        
        add_capture(job_id,iface,proto,src,dst,duration,bucket)


        return '''<h1>Inteface: {}</h1>
                  <h1>Protocol: {}</h1>
                  <h1>Source: {}</h1>
                  <h1>Destination: {}</h1>
                  <h1>Duration in Seconds: {}</h1>
                  <h1>AWS S3 Bucket: {}</h1>'''.format(iface, proto, src, dst, duration, bucket)

    return '''<form method="POST">
                  Interface: <input type="text" name="iface"><br>
                  Protocol: <input type="text" name="proto"><br>
                  Source: <input type="text" name="src"><br>
                  Destination: <input type="text" name="dst"><br>
                  Duration: <input type="text" name="duration"><br>
                  Bucket: <input type="text" name="bucket"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/status', methods=['GET', 'POST'])
def pcap_status():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        job_id = request.form['job_id']
        get_capture(job_id)
        id, job_id, iface, proto, src, dst, duration, bucket, filename, url, status = get_capture(job_id)
        job = id, job_id, iface, proto, src, dst, duration, bucket, filename, url, status

        return '''<h1>Status: {}</h1>'''.format(job[10])

    return '''<form method="POST">
                Enter Job ID: <input type="text" name="job_id"><br>
                <input type="submit" value="Submit"><br>
            </form>'''

@app.route('/pcap_json', methods=['POST'])
def run_pcap_json():
    req_data = request.get_json()
    job_id = randint(100000,999999)
    job = str(job_id)
    iface = req_data['iface']
    proto = req_data['proto']
    src = req_data['src']
    dst = req_data['dst']
    duration = req_data['duration']
    bucket = req_data['bucket']
    add_capture(job_id,iface,proto,src,dst,duration,bucket)
    return jsonify( {'job_id': job} )

@app.route('/status_json', methods=['POST'])
def status_json():
    req_data = request.get_json()
    job_id = req_data['job_id']
    id, job_id, iface, proto, src, dst, duration, bucket, filename, url, status = get_capture(job_id)
    return jsonify( {'job_id': job_id, 'iface': iface, 'proto': proto, 'src': src, 'dst': dst, 'duration': duration, 'url': url, 'status': status} )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
