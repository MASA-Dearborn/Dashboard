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
    """Converts a string of hex characters to a list of bytes."""
    
    bytlst = []
    for i in range(int(len(hexstr) / 2)):
        byt = int(hexstr[i*2:i*2+2], 16)
        bytlst.append(byt)
    
    return bytlst

def main():
    parser = argparse.ArgumentParser() # Parser for command line arguments

    parser.add_argument("--fps", type=int, default=30, help="FPS to capture video at")
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate for USB")
    parser.add_argument("--com", type=str, default="COM1", help="Serial port to send video on")
    parser.add_argument("--quality", type=lambda x: max(0, int(x)), default=50, help="JPEG quality to compress to")
    parser.add_argument("--header", type=int, default=127, help="Start byte to attach to packet")

    args = parser.parse_args()

    camera = PiCamera() # Raspberry Pi Camera reader
    capture = PiRGBArray() # Array to store capture

    encoded_params = [int(cv2.IMWRITE_JPEG_QUALITY), args.quality] # Encoding parameters for opencv 

    ser = serial.Serial(args.com, args.baud) # Serial writer
    header = args.header # Start byte

    crc_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF) # CRC-32 function

    time.sleep(0.1) # Sleep for the camera to get warmed up

    while True:
        camera.capture(capture, format="bgr") # Capture a frame
        image = capture.array   # Convert to numpy array

        frame = cv2.imencode(".jpg", image, encoded_params) # Encode image to jpeg

        frame_array = [frame[i][0] for i in range(len(frame))] # Turn jpeg format into one-dimensional list
        length_array = list(struct.pack(">I", len(frame_array) + 9) # Construct a list of packed binary data corresponding to length of packet
        temp_list = bytearray([header] + length_array + frame_array + [0, 0, 0, 0]) # Create packet with empty crc
        complete_list = bytearray([header] + length + frame_array + convert_hex_to_bytelist(hex(crc_func(byte_list)))) # Attach crc remainder to packet
        ser.write(complete_list) # Write the entire packet to the serial port

        time.sleep(1 / args.fps) # Sleep for some amount of time


if __name__ == "__main__":
    main()