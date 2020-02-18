# Raspberry Pi Video Capture
# By Dean Lawrence and Megan Terberg

from picamera import PiCamera 
from picamera.array import PiRGBArray

import time
import cv2
import argparse
import serial
import crcmod

def convert_hex_to_bytelist(hex_in):
    bytlst = []
    for i in range(int(len(hexstr) / 2)):
        byt = int(hexstr[i*2:i*2+2], 16)
        bytlst.append(byt)
    
    return bytlst

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", help="Path to configuration file")

    args = parser.parse_args()

    camera = PiCamera()
    capture = PiRGBArray()

    ser = serial.Serial("COM1", 9600)

    time.sleep(0.1)

    while True:
        camera.capture(capture, format="bgr")
        frame = capture.array

        frame_array = [frame[i][0] for i in range(len(frame))]
        length_array = list(struct.pack(">I", len(frame_array) + 9)
        header = 127
        temp_list = bytearray([header] + length_array + frame_array + [0, 0, 0, 0])
        complete_list = bytearray([header] + length + frame_array + convert_hex_to_bytelist(hex(crc_func(byte_list))))
        serial.Serial("COM1", 9600).write(complete_list)

        time.sleep(1 / 30)


if __name__ == "__main__":
    main()