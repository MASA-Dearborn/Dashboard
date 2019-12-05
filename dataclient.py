# Data client

import argparse
import json

from masalib import DataSerialReader, TeleGPSSerialReader, EggFinderSerialReader
from masalib import PacketSender

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = json.loads(fp.read())

    receiver_list = []

    receiver_list.append(DataSerialReader("COM1", 9600, header_byte=0, start_byte=126, stop_byte=127))
    receiver_list.append(TeleGPSSerialReader("COM2", 9600, header_byte=1))
    receiver_list.append(EggFinderSerialReader("COM3", 9600, header_byte=2))

    sender = PacketSender("127.0.0.1", 9990)

    while True:
        for receiver in receiver_list:
            sender.send_next_serial_packet(receiver)
    
    sender.close_socket()

    sender.plot_latency_list(args.latency)
    sender.plot_drop_rate_list(args.droprate)


if __name__ == "__main__":
    main()

