# MASA Dashboard Video Client
# By Dean Lawrence

import argparse
import socket
import cv2
import pickle
import time
import struct
#import crcmod
import numpy as np
import serial

def convert_hex_to_bytelist(hex_in):
    bytlst = []
    for i in range(int(len(hexstr) / 2)):
        byt = int(hexstr[i*2:i*2+2], 16)
        bytlst.append(byt)

    return bytlst

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", help="Local path to configuration file")

    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9992))
    connection = client_socket.makefile('wb')

    capture = cv2.VideoCapture(0) # video capture class, frame by frame, takes
    # either from an mp4 file or the device index (0 is the first camera/webcam)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH,360)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]


    # CRC-32
    #crc_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)

    # Set jpg numpy array to bytestring
    #frame_array = [frame[i][0] for i in range(len(frame))]
    #length = list(struct.pack(">I", len(frame_array) + 9)
    #header = 127
    #temp_list = bytearray([header] + length + frame_array + [0, 0, 0, 0])
    #complete_list = bytearray([header] + length + frame_array + convert_hex_to_bytearray(hex(crc_func(byte_list))))
    #serial.Serial("COM1", 9600).write(complete_list)

    # Set bytestring to jpg in correct shape
    #arr = list(complete_list)
    #img = np.array([np.array([i]) for i in arr])




    while True:
        _, frame = capture.read()

        _, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
