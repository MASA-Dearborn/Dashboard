
import time
import struct

from masalib import PacketSender


def main():
    sender = PacketSender("127.0.0.1", 9990)

    while True:
        sender.send_spoof_packet([34, 128, 100, 34, 128, 64, 4, 0], "10001001", header=0)
        sender.send_spoof_packet([0, 0, 100, 34, 128, 32, 0, 0], "10001001", header=1)
        time.sleep(1)

if __name__ == "__main__":
    main()