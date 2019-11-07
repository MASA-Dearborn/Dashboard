# Data client

import argparse
import json

from masalib import SerialReader
from masalib import PacketSender

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    sender_list = []

    data_reader = SerialReader("COM1", 9600, start_byte=126, stop_byte=127)
    data_sender = PacketSender("127.0.0.1", 9990, serial_reader=data_reader)
    sender_list.append(data_sender)

    gps_reader = SerialReader("COM2", 9600, start_byte=126, stop_byte=127)
    gps_sender = PacketSender("127.0.0.1", 9990, serial_reader=gps_reader)
    sender_list.append(gps_sender)

    video_reader = SerialReader("COM3", 9600, start_byte=126, stop_byte=127)
    video_sender = PacketSender("127.0.0.1", 9990, serial_reader=video_reader)
    sender_list.append(video_sender)

    while True:
        for sender in sender_list:
            sender.send_next_serial_packet()
    
    sender.close_socket()

    sender.plot_latency_list(args.latency)
    sender.plot_drop_rate_list(args.droprate)


if __name__ == "__main__":
    main()

