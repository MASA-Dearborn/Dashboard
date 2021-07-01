# MASA Dashboard Web Server
# By Dean Lawrence

import argparse #parser for the command-line arguement which allows for the addition
#of the config file
import json #json encoder and decoder library, used for the config file
import sqlite3
import threading
import cv2
import struct
import pickle
import socket
import queue

from flask import request
from flask import Response
from flask import jsonify
from flask import render_template
from flask import Flask

from flask_cors import CORS, cross_origin

video_output_frame = None
video_lock = threading.Lock()

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

def receive_video():
    global video_output_frame, video_lock

    HOST='127.0.0.1'
    PORT=9992

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn,addr=s.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    #print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            #print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        #print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        #print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        with video_lock:
            video_output_frame = frame.copy()


def generate_frame():
    global video_output_frame, video_lock

    while True:
        with video_lock:
            if video_output_frame is None:
                continue

            flag, encoded_image = cv2.imencode(".jpg", video_output_frame)

            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			    bytearray(encoded_image) + b'\r\n')


@app.route('/')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def index():
    return render_template("index.html")

@app.route('/config')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def config():
    return jsonify(tables_list)

@app.route('/fetch')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch():
    response = {}
    with sqlite3.connect("test_database.db") as conn:
        for table in tables_list:
            c = conn.cursor()
            c.execute("SELECT * FROM " + table + " ORDER BY id DESC LIMIT 1;")
            response[table] = list(c.fetchone())

    return jsonify(response)

@app.route('/video')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def video():
    return Response(generate_frame(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    parser = argparse.ArgumentParser() #creates the argument parser for the config file

    parser.add_argument("-c", "--config", type=str, required=True, help="Path to configuration file")
    #adds the config file argument to the argument parser

    args = parser.parse_args() #runs the argument parser, asking for the config file

    with open(args.config, "r") as fp: #open up the config file in read format
        config = json.loads(fp.read())["server"] #open up the server section of the config file

    tables_list = config["tables"]

    video_thread = threading.Thread(target=receive_video)
    video_thread.daemon = True
    video_thread.start()

    app.run(host=config["ip"], port='5000', debug=True, threaded=True, use_reloader=False)
