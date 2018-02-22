from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from capture import *
from get_capture import *
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
        filename = request.form['filename']
        add_capture(job_id,iface,proto,src,dst,duration,bucket,filename)


        return '''<h1>Inteface: {}</h1>
                  <h1>Protocol: {}</h1>
                  <h1>Source: {}</h1>
                  <h1>Destination: {}</h1>
                  <h1>Duration in Seconds: {}</h1>
                  <h1>AWS S3 Bucket: {}</h1>
                  <h1>Filename: {}</h1>'''.format(iface, proto, src, dst, duration, bucket, filename)

    return '''<form method="POST">
                  Interface: <input type="text" name="iface"><br>
                  Protocol: <input type="text" name="proto"><br>
                  Source: <input type="text" name="src"><br>
                  Destination: <input type="text" name="dst"><br>
                  Duration: <input type="text" name="duration"><br>
                  Bucket: <input type="text" name="bucket"><br>
                  Filename: <input type="text" name="filename"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/status', methods=['GET', 'POST'])
def pcap_status():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        job_id = request.form['job_id']
        get_capture(job_id)


        return '''<h1>Enter Job ID: {}</h1>'''.format(job_id)

    return jsonify({result})

@app.route('/pcap_json/', methods=['POST'])
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
    filename = req_data['filename']
    add_capture(job_id,iface,proto,src,dst,duration,bucket,filename)
    return "This is your job ID: " + job

@app.route('/pcap_json/', methods=['GET'])
def status_json():
    req_data = request.get_json()
    job_id = req_data['job_id']
    get_capture(job_id)
    return result
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
