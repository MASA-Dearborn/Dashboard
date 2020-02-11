# MASA Dashboard Video Client
# By Dean Lawrence

import argparse
import socket
import cv2
import pickle
import time
import struct

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", help="Local path to configuration file")

    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9992))
    connection = client_socket.makefile('wb')

    capture = cv2.VideoCapture(0)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH,480)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,360)

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

    while True:
        ret, frame = capture.read()
        
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        time.sleep(1 / 30)
	

if __name__ == "__main__":
    main()