# Data client

import argparse
import json

from masalib import SerialReader
from masalib import PacketSender

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ip", type=str, default="199.223.115.24", help="IP to send packets to")
    parser.add_argument("--port", type=int, default=9992, help="Port to send packets to")
    parser.add_argument("--bytes", type=int, help="Number of data bytes to send in a packet")
    parser.add_argument("--packets", type=int, help="Number of packets to send")
    parser.add_argument("--crc", type=str, help="CRC to use for error checking")
    parser.add_argument("--latency", type=str, default="latency_plot.png", help="File to save latency plot to")
    parser.add_argument("--droprate", type=str, default="drop_rate_plot.png", help="File to save drop rate plot to")

    args = parser.parse_args()

    sender = PacketSender(args.ip, args.port)

    for i in range(args.packets):
        print("----", i, "----")
        sender.send_random_packet(args.bytes, args.crc, i)
    
    sender.close_socket()

    sender.plot_latency_list(args.latency)
    sender.plot_drop_rate_list(args.droprate)


if __name__ == "__main__":
    main()

