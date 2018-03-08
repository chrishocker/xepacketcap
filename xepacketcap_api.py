from flask import Flask, url_for, jsonify, request
#from flask_sqlalchemy import SQLAlchemy
from capture import *
#from threading import Thread
from random import randint


app = Flask(__name__)

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
